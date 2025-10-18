
from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Role Model (e.g., Administrator, Seller, Buyer)
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# 2. Custom User Model
class User(AbstractUser):
    # Link to the Role model
    role = models.ForeignKey(
        Role, 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True
    )
    # Custom fields for profile data
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True)
    
    # Use email as the main identifier for the user:
    email = models.EmailField(unique=True, blank=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name'] 

    def __str__(self):
        return self.email