from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    """
    Post serializer.
    
    Serializes post data including author information.
    Returns both author username and ID for frontend reference.
    """
    author_id = serializers.ReadOnlyField(source='author.id')  # Return author_id 
    author = serializers.ReadOnlyField(source='author.username')  # Return username
    author_profile_image = serializers.SerializerMethodField()  # 프로필 이미지 필드 추가

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'author_id', 'author_profile_image', 'created_at']

    def get_author_profile_image(self, obj):
        """
        사용자의 프로필 이미지 URL을 가져옵니다.
        """
        from mypage.models import UserProfile
        try:
            # 사용자 프로필 정보 조회
            profile = UserProfile.objects.get(user=obj.author)
            return profile.profile_image.url if profile.profile_image else None
        except UserProfile.DoesNotExist:
            return None

class CommentSerializer(serializers.ModelSerializer):
    """
    Comment serializer.
    
    Serializes comment data including author information.
    Author and post fields are read-only to prevent modification.
    """
    author_id = serializers.ReadOnlyField(source='author.id')  # Author ID field
    author = serializers.ReadOnlyField(source='author.username')  # Author field is read-only
    author_profile_image = serializers.SerializerMethodField()  # 프로필 이미지 필드 추가

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'author_id', 'author_profile_image', 'post', 'created_at']  # Include post field
        read_only_fields = ['post', 'author']  # Set post and author as read-only
        
    def get_author_profile_image(self, obj):
        """
        사용자의 프로필 이미지 URL을 가져옵니다.
        """
        from mypage.models import UserProfile
        try:
            # 사용자 프로필 정보 조회
            profile = UserProfile.objects.get(user=obj.author)
            return profile.profile_image.url if profile.profile_image else None
        except UserProfile.DoesNotExist:
            return None