# users/serializers.py (REPLACED/SIMPLIFIED)

from rest_framework import serializers
from .models import User 

class UserRegistrationSerializer(serializers.ModelSerializer):
    # Only need the three fields from the frontend
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        # The frontend only provides these fields:
        fields = ('email', 'username', 'password') 
        # is_active will default to True, allowing login immediately as a Buyer.
        
    def create(self, validated_data):
        # 1. Pop the raw password for explicit handling
        password = validated_data.pop('password')
        
        # 2. POP EMAIL AND USERNAME
        # We must remove 'email' and 'username' from validated_data 
        # because we are passing them as explicit keyword arguments below.
        email = validated_data.pop('email') 
        username = validated_data.pop('username')

        # 3. Create the user
        user = User.objects.create_user(
            # Pass mandatory fields explicitly
            email=email,
            username=username,
            password=password,
            # Pass any remaining fields (like first_name, last_name, though not in your current fields)
            # which is an empty dict now, but is safe.
            **validated_data 
        )
        return user