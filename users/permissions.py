# users/permissions.py

from rest_framework import permissions

# 1. Permission for Admin ONLY access
class IsAdminUser(permissions.BasePermission):
    """ Custom permission to only allow 'Admin' users to access the view. """
    def has_permission(self, request, view):
        # Relies on the .is_admin property from users/models.py
        return bool(request.user and request.user.is_admin) 

# 2. Permission for Admin OR Owner access (for self-management)
class IsAdminOrOwner(permissions.BasePermission):
    """ Allows 'Admin' users OR the object owner. Used for User self-management. """
    
    # Check if the user is authenticated (handled by the view)
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Admin users can access any object
        if request.user.is_admin:
            return True
        
        # Buyers/Owners can only update/delete their own user object
        # The obj here is the User instance being requested (e.g., /users/5/)
        return obj == request.user

# 3. Permission for Item CRUD (Admin only for POST/PUT/DELETE)
class IsAdminOnlyForWrite(permissions.BasePermission):
    """ Allows everyone to read (GET), but only Admin to CUD (POST, PUT, DELETE) items. """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # Allow Read (GET, HEAD, OPTIONS) for everyone (Authenticated or not)
            return True
        
        # Require ADMIN for Create, Update, Delete
        return bool(request.user and request.user.is_admin)