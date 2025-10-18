# users/urls.py

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserRegistrationView

urlpatterns = [
    # Custom Registration Endpoint
    path('auth/register/', UserRegistrationView.as_view(), name='register'),
    
    # 1. JWT Login Endpoint (Token Generation)
    # This view handles validation and issues the JWT Access and Refresh tokens.
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # 2. JWT Token Refresh Endpoint
    # Allows users to get a new Access token using their valid Refresh token.
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]