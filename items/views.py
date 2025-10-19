# items/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from users.serializers import UserProfileSerializer 
from users.models import User
from .models import Item, Category
from .serializers import ItemSerializer, CategorySerializer
from users.permissions import IsAdminOnlyForWrite # Import the custom permission

class DashboardView(APIView):
    """
    Dashboard endpoint: Returns user-specific data based on their role.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        role_name = user.role.name # Assuming role name is accessible here
        
        # 1. Base Data: Profile and Role
        data = {
            'profile': UserProfileSerializer(user).data,
            'role': role_name,
            'dashboard_content': {}
        }
        
        # 2. Dynamic Content Logic
        
        if role_name == 'Administrator':
            # Admin Dashboard: Global oversight
            admin_content = {
                'total_users': User.objects.count(),
                'total_active_listings': Item.objects.filter(is_available=True).count(),
                'recent_listings': ItemSerializer(Item.objects.all().order_by('-created_at')[:5], many=True).data,
            }
            data['dashboard_content'] = admin_content
        
        elif role_name == 'Seller':
            # Seller Dashboard: Their listings and sales
            seller_items = Item.objects.filter(seller=user).order_by('-created_at')
            seller_content = {
                'my_listings_count': seller_items.count(),
                'my_active_listings': ItemSerializer(seller_items.filter(is_available=True), many=True).data,
                'pending_orders': 0, # To be implemented
            }
            data['dashboard_content'] = seller_content
            
        else: # Buyer and Moderator use a simpler view for now
            # Buyer/Moderator Dashboard: Default view
            data['dashboard_content'] = {
                'message': f"Welcome, {user.username}! Your dashboard features are still under construction."
            }
            
        return Response(data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows categories to be viewed.
    Read-only for all users (Admin creates them via Django Admin).
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows items to be viewed, created, updated, or deleted.
    - Everyone can READ (GET).
    - Only Admin can WRITE (POST, PUT, DELETE).
    """
    queryset = Item.objects.filter(is_available=True).order_by('-created_at') # Only show available items
    serializer_class = ItemSerializer
    
    # Allows anyone to read (IsAuthenticatedOrReadOnly)
    # IsAdminOnlyForWrite enforces that POST/PUT/DELETE requires an Admin
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOnlyForWrite] 

    def perform_create(self, serializer):
        # When an Admin creates an item, automatically set the seller to the Admin user
        serializer.save(seller=self.request.user)
    
    def get_queryset(self):
        # Admins can see all items, including unavailable ones (for management)
        if self.request.user.is_authenticated and self.request.user.is_admin:
            return Item.objects.all().order_by('-created_at')
        # Buyers/Unauthenticated users only see available items
        return Item.objects.filter(is_available=True).order_by('-created_at')