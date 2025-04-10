from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like


CustomUser = get_user_model()


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'created_at']
        read_only_fields = ['id','user', 'created_at', 'updated_at']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # Display username
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), write_only=True) # To create comment on a specific post

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField() 
    like_count = serializers.SerializerMethodField()  
    comments = CommentSerializer(many=True, read_only=True) 
    
    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'created_at', 'updated_at', 'like_count', 'comments']
    
    # Calculate the number of likes for the post
    def get_like_count(self, obj):
        return obj.likes.count()

