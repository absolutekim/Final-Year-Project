from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# User profile model for storing additional user information
class UserProfile(models.Model):
    """
    User profile model.
    
    Extends the default User model with additional profile information and customization options.
    Provides fields for personal details, profile image, and biographical information.
    Each profile is associated with exactly one user account.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Associated user account (one-to-one)
    nickname = models.CharField(max_length=50, blank=True)  # User's public display name
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)  # User's profile picture
    bio = models.TextField(blank=True)  # User's biographical information/description
    updated_at = models.DateTimeField(auto_now=True)  # When the profile was last updated (automatic)

    def __str__(self):
        return f"{self.user.username}'s profile"
