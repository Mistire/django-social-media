from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LikeViewSet, PostListView, CommentViewSet, PostDetailView


router = DefaultRouter()
router.register(r'', PostListView, basename='post')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:post_pk>/like/', LikeViewSet.as_view({'post': 'create'}), name='post-like'),
    path('<int:post_pk>/comment/', CommentViewSet.as_view({'post': 'create'}), name='post-comment'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
]
