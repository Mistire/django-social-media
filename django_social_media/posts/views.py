
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from rest_framework.permissions import IsAuthenticatedOrReadOnly, generics, permissions
from .models import Post
from .serializers import PostSerializer


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostListView(generics.RetrieveAPIView):
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
            raise PermissionDenied("You don't have permission to edit this post.")
        serializer.save(updated_at=timezone.now())

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You don't have permission to delete this post.")
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Post deleted successfully"}, status=status.HTTP_200_OK)

