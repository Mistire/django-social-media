from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostListView, CommentViewSet

router = DefaultRouter()
router.register(r'posts', PostListView, basename='post')

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_pk>/comment/', CommentViewSet.as_view({'post': 'create'}), name='post-comment'),
]

