
from django.contrib.auth import get_user_model
from .models import Post, Comment


CustomUser = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id','user', 'created_at', 'updated_at']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # Display username
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), write_only=True) # To create comment on a specific post

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'text', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

