from django.shortcuts import render
from django.urls import path
from .views import register_user, CustomTokenObtainPairView, debug_login, get_subcategory_tags, get_user_profile, update_user_tags, delete_user_account
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', register_user, name='register'),  # User registration API
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # ✅ Custom login implementation
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token refresh endpoint
    path('debug-login/', debug_login, name='debug_login'),  # ✅ Debug login endpoint
    path('tags/', get_subcategory_tags, name='get_subcategory_tags'), # ✅ Added API path for subcategory tags
    path('profile/', get_user_profile, name='get_user_profile'), # ✅ Added API path for user profile
    path('update-tags/', update_user_tags, name='update_user_tags'), # ✅ Added API path for updating user tags
    path('delete-account/', delete_user_account, name='delete_user_account'),  # Account deletion API
]
