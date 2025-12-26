from django.urls import path
from .views import MyPageViewSet

# URL patterns for the mypage app
urlpatterns = [
    # Profile endpoints
    path('profile/', MyPageViewSet.as_view({
        'get': 'retrieve',  # GET request to retrieve user profile
        'put': 'update'     # PUT request to update user profile
    })),
]
