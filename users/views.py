
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer

class UserRegistrationView(generics.CreateAPIView):
    """
    API view for user registration.
    Allows unauthenticated users to register.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny] 