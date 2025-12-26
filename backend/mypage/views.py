from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import UserProfile
from .serializers import UserProfileSerializer
from django.shortcuts import get_object_or_404

# ViewSet for handling user profile operations
class MyPageViewSet(viewsets.ViewSet):
    """
    ViewSet to handle user profile operations.
    Provides endpoints for retrieving and updating user profile information.
    Requires authentication for all operations.
    """
    permission_classes = [permissions.IsAuthenticated]  # User must be logged in to access these endpoints

    def retrieve(self, request):
        """
        Retrieves the profile of the currently authenticated user.
        
        Returns:
            Response with serialized user profile data or error message.
        """
        try:
            profile = get_object_or_404(UserProfile, user=request.user)  # Get profile for the current user
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request):
        """
        Updates the profile of the currently authenticated user.
        Supports partial updates for individual fields.
        
        Returns:
            Response with updated profile data or validation errors.
        """
        try:
            profile = get_object_or_404(UserProfile, user=request.user)  # Get profile for the current user
            
            # Handle age_group and gender update - update the user model directly
            if 'age_group' in request.data:
                user = request.user
                user.age_group = request.data.get('age_group')
                user.save()
                
            # Handle gender update
            if 'gender' in request.data:
                user = request.user
                user.gender = request.data.get('gender')
                user.save()
                
            # Update other profile fields through serializer
            serializer = UserProfileSerializer(
                profile, 
                data=request.data, 
                partial=True  # Allow partial updates (only provided fields will be updated)
            )
            if serializer.is_valid():
                serializer.save()
                # Return fresh data after update
                updated_serializer = UserProfileSerializer(profile)
                return Response(updated_serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
