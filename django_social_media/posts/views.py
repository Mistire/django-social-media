
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer



CustomUser = get_user_model()
#class PostCreateView(generics.CreateAPIView):
#    queryset = Post.objects.all()
#    serializer_class = PostSerializer
#    permission_classes = [permissions.IsAuthenticated]

#    def perform_create(self, serializer):
#        serializer.save(user=self.request.user)

class PostListView(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action == 'list':
            return Post.objects.all().order_by('-created_at')
        return Post.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        post = self.get_object()
        if post.user != self.request.user:
            raise PermissionDenied(
                "You don't have permission to edit this post.")
        serializer.save(updated_at=timezone.now())

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied(
                "You don't have permission to delete this post.")
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Post deleted successfully"}, status=status.HTTP_200_OK)


class LikeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, post_pk=None):
        post = get_object_or_404(Post, id=post_pk)
        like, created = Like.objects.get_or_create(
            post=post, user=request.user)

        if not created:
            like.delete()
            message = "Unliked"
        else:
            message = "Liked"

        return Response({
            "message": message,
            "like_count": post.likes.count()
        }, status=status.HTTP_200_OK)

class CommentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def create(self, request, post_pk=None):
        post = get_object_or_404(Post, id=post_pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
