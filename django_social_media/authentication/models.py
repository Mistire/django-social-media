from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
  def create_user(self, email, username, password=None, **extra_fields):
    if not email:
      raise ValueError("Email is required")
    email = self.normalize_email(email)
    user = self.model(email=email, username=username, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    date_joined = models.DateTimeField(auto_now_add=True)
    return user
  
  def create_superuser(self, email, username, password=None, **extra_fields):
    extra_fields.setdefault("is_staff", True)
    extra_fields.setdefault('is_superuser', True)
    return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField(max_length=255, unique=True)
  username = models.CharField(max_length=255, unique=True)
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  date_joined = models.DateTimeField(default=timezone.now)
  
  objects = CustomUserManager()

  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = ["username"]

  def __str__(self):
    return self.email
  


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, related_name="following", on_delete=models.CASCADE)
    following = models.ForeignKey(CustomUser, related_name="followers", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ("follower", "following")
        ordering = ["-created_at"]

    
    def __str__(self):
        return f"{self.follower} follows {self.following}"