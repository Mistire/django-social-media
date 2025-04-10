from django.shortcuts import get_object_or_404, render
from posts.serializers import PostSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import FollowSerializer, RegisterSerializer, LoginSerializer, TokenObtainPairSerializer, ProfileSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .models import Follow, Profile
from posts.models import Post
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class RegisterView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            Profile.objects.create(user=user)  # Create a profile for the user
            return Response({"message": "User registered successfully and profile created."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
            },
            required=['refresh_token']
        )
    )
    def post(self, request):
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return Response({"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = TokenObtainPairSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProfileRetrieveUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)


class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        following_user = get_object_or_404(CustomUser, id=user_id)

        if request.user == following_user:
            return Response(
                {"error": "You cannot follow yourself"},  
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if Follow.objects.filter(follower=request.user, following=following_user).exists():
            return Response(
                {"error": "You are already following this user"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        follow = Follow.objects.create(follower=request.user, following=following_user)
        serializer = FollowSerializer(follow, context={'request': request})
        
        return Response(
            {"message": f"You are now following {following_user.username}"},
            status=status.HTTP_201_CREATED
        )


class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        following_user = get_object_or_404(CustomUser, id=user_id)

        try:
            follow = Follow.objects.get(
                follower=request.user,
                following = following_user
            )
            follow.delete()
            return Response(
                {"message": f"You have unfollowed {following_user.username}"},
                status=status.HTTP_200_OK)
        except Follow.DoesNotExist:
            return Response(
                {"error": "You are not following this user."},
                status=status.HTTP_400_BAD_REQUEST
                )

class FollowersListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        followers = CustomUser.objects.filter(following__following=user)
        serializer = ProfileSerializer(followers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FollowingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        following = CustomUser.objects.filter(followers__follower=user)
        serializer = ProfileSerializer(following, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        followed_users = request.user.following.values_list('following_id', flat=True)
        posts = Post.objects.filter(user__in=followed_users).order_by('-created_at')

        serializers = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)