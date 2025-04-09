from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostListView

router = DefaultRouter()
router.register(r'posts', PostListView, basename='post')

urlpatterns = [
    path('', include(router.urls)),
    ]
