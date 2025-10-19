# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Role # Import your custom models

# ----------------------------------------------------
# 1. Custom Admin for the User Model
# ----------------------------------------------------
class UserAdmin(BaseUserAdmin):
    # The fields to show in the list view
    list_display = ('id', 'email', 'username', 'role', 'is_staff', 'date_joined')
    
    # The fields to use as filters on the right sidebar
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    
    # The fields to allow searching by
    search_fields = ('email', 'username')
    
    # The fields shown on the user detail page (edit form)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'first_name', 'last_name', 'phone_number', 'bio', 'wallet_balance')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Roles', {'fields': ('role',)}) # Show the custom role field
    )
    
    # Ensures the custom fields are correctly ordered when creating a user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password', 'password2', 'role'),
        }),
    )

    # Automatically set the 'role' field to be visible in the list and detail views
    ordering = ('email',)


# ----------------------------------------------------
# 2. Register Models
# ----------------------------------------------------

# Register the custom User model with the custom admin class
admin.site.register(User, UserAdmin)

# Register the Role model so you can manage the 'Admin' and 'Buyer' roles
admin.site.register(Role)