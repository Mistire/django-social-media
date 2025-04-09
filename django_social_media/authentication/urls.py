from django.urls import path
from .views import FollowUserView, RegisterView, LogoutView, UnfollowUserView, UserLoginView, UserProfileView, ProfileRetrieveUpdateView, FollowersListView, FollowingListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/me/', UserProfileView.as_view(), name='my_profile'),
    path('profile/<int:pk>/', ProfileRetrieveUpdateView.as_view(), name='user_profile'),
    path('users/<int:user_id>/follow/', FollowUserView.as_view(), name="follow-user"),
    path('users/<int:user_id>/unfollow/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('users/<int:user_id>/followers/', FollowersListView.as_view(), name='user-followers'),
    path('users/<int:user_id>/following/', FollowingListView.as_view(), name='user-following'),
]
