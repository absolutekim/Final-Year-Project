from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

# Serializer for the User model with limited fields for security
class UserSerializer(serializers.ModelSerializer):
    """
    User data serializer.
    
    Serializes the User model with only essential fields for security.
    Provides a limited public view of user data, excluding sensitive information.
    All fields are read-only to prevent unauthorized modification through this serializer.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'age_group', 'gender')
        read_only_fields = ('id', 'username', 'email')  # These fields cannot be modified through this serializer

# Serializer for the UserProfile model including the related User data
class UserProfileSerializer(serializers.ModelSerializer):
    """
    User profile serializer.
    
    Serializes the UserProfile model with nested User information.
    Used for retrieving and updating user profile information including 
    nickname, profile image, and biographical information.
    Includes the associated user data but prevents modification of user fields.
    """
    user = UserSerializer()  # Nested serializer for the related User model
    
    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'nickname', 'profile_image', 'bio', 'updated_at')
        read_only_fields = ('id', 'user', 'updated_at')  # These fields cannot be modified through this serializer
