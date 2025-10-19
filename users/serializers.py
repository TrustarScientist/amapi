# users/serializers.py (REPLACED/SIMPLIFIED)

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Role 

class UserRegistrationSerializer(serializers.ModelSerializer):
    # Only need the three fields from the frontend
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        # The frontend only provides these fields:
        fields = ('email', 'username', 'password') 
        # is_active will default to True, allowing login immediately as a Buyer.
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data.pop('email') 
        username = validated_data.pop('username')

        # 1. Create the user
        user = User.objects.create_user(
            email=email,
            username=username,
            password=password,
            **validated_data 
        )
        
        # 2. Assign the default 'Buyer' role
        # IMPORTANT: This assumes the 'Buyer' Role instance already exists in the database.
        try:
            buyer_role = Role.objects.get(name='Buyer')
            user.role = buyer_role
            user.save()
        except Role.DoesNotExist:
            # Handle error if roles are not yet created in the DB (use a proper logger in prod)
            print("WARNING: 'Buyer' role not found. User assigned a null role.")
        
        return user
    

class UserProfileSerializer(serializers.ModelSerializer):
    # This field will show the name of the role instead of just the ID
    role_name = serializers.CharField(source='role.name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 
            'email', 
            'username', 
            'role', 
            'role_name',
            # Add other profile fields you want visible on the dashboard (e.g., 'date_joined')
        ]
        read_only_fields = ['email', 'username', 'role'] # These fields shouldn't be edited via the profile view


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Customizes the login response to include user info and role.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims to the token payload (optional, but useful)
        token['role'] = user.role.name if user.role else 'None'
        token['is_admin'] = user.is_admin
        
        return token

    def validate(self, attrs):
        # The default validate method handles authentication and token generation
        data = super().validate(attrs)

        # 1. Add the tokens to the response data
        # data['access'] = self.validated_data['access']
        # data['refresh'] = self.validated_data['refresh']
        
        # 2. Add custom user info to the response
        user = self.user
        data['user_info'] = {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'role': user.role.name if user.role else 'None', # Include the user role
            'is_admin': user.is_admin,
            'wallet_balance': user.wallet_balance,
        }
        
        return data