
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework import viewsets
from .models import User
from .serializers import UserProfileSerializer
from .permissions import IsAdminOrOwner 
from rest_framework.permissions import IsAuthenticated

class UserRegistrationView(generics.CreateAPIView):
    """
    API view for user registration.
    Allows unauthenticated users to register.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny] 


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Uses the custom serializer to return user info along with tokens on login.
    """
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOwner]