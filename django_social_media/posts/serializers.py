from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
