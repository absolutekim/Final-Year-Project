from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.serializers import RegisterSerializer
from django.contrib.auth import authenticate
from django.db import connection
from accounts.models import CustomUser

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT token view that extends the default TokenObtainPairView.
    Returns username along with the JWT tokens for better client-side user management.
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Authenticate the logged-in user
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)  # Authentication process

        if user is None:
            return Response({"error": "Invalid credentials"}, status=401)  # Return 401 on authentication failure

        # Return username instead of user_id in the response
        response.data['username'] = user.username  

        return response

@api_view(['POST'])
@permission_classes([AllowAny])
def debug_login(request):
    """
    Debug login endpoint for testing authentication.
    Authenticates a user without issuing JWT tokens.
    
    Parameters:
        request: HTTP request with username and password
        
    Returns:
        Response with success/error message and appropriate status code
    """
    username = request.data.get('username')
    password = request.data.get('password')

    print(f"🛠 DEBUG: username={username}, password={password}")  # Debug log

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({"error": "Invalid username or password"}, status=401)

    return Response({"message": "Login successful!"}, status=200)


@api_view(['POST'])
@permission_classes([AllowAny])  # Allow access without authentication
def register_user(request):
    """
    User registration endpoint.
    Creates a new user account using the provided data.
    
    Parameters:
        request: HTTP request with user registration data
        
    Returns:
        Response with success/error message and appropriate status code
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_subcategory_tags(request):
    """
    API to retrieve travel destination tags - extracting only subcategory0.
    Gets a list of unique subcategories from the destinations database.
    
    Parameters:
        request: HTTP request
        
    Returns:
        Response with list of subcategory tags
    """
    with connection.cursor() as cursor:
        # Query to extract only the exact subcategory0 list
        cursor.execute("""
            SELECT DISTINCT json_extract(subcategories, '$[0]') AS first_subcategory
            FROM destinations_location
            WHERE json_extract(subcategories, '$[0]') IS NOT NULL
            ORDER BY first_subcategory;
        """)
        subcategories = [row[0] for row in cursor.fetchall() if row[0]]
        
        print("Extracted subcategory0 list:", subcategories)
    
    return Response({"tags": subcategories}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """
    API to retrieve profile information of the logged-in user.
    Returns user data including username, email, nickname, gender, and selected tags.
    
    Parameters:
        request: HTTP request with authenticated user
        
    Returns:
        Response with user profile data
    """
    user = request.user
    
    return Response({
        "username": user.username,
        "email": user.email,
        "nickname": user.nickname,
        "gender": user.gender,
        "selected_tags": user.selected_tags
    }, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_tags(request):
    """
    API to update user's tag information.
    Updates the user's selected tags with validation for tag count.
    
    Parameters:
        request: HTTP request with authenticated user and new tags
        
    Returns:
        Response with success/error message and updated tags
    """
    user = request.user
    selected_tags = request.data.get('selected_tags', [])
    
    # Validate tag count
    if len(selected_tags) < 3 or len(selected_tags) > 7:
        return Response({"error": "You must select between 3 and 7 tags."}, status=status.HTTP_400_BAD_REQUEST)
    
    user.selected_tags = selected_tags
    user.save()
    
    return Response({
        "message": "Tags have been successfully updated.",
        "selected_tags": user.selected_tags
    }, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user_account(request):
    """
    API to delete a user account.
    Deletes the user account after confirming password.
    
    Parameters:
        request: HTTP request with authenticated user and password confirmation
        
    Returns:
        Response with success/error message and appropriate status code
    """
    user = request.user
    
    # Password confirmation
    password = request.data.get('password')
    if not password:
        return Response({"error": "Please enter your password."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Password validation
    if not user.check_password(password):
        return Response({"error": "Password does not match."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Account deletion
    try:
        user.delete()
        return Response({"message": "Your account has been successfully deleted."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

