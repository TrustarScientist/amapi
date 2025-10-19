# items/admin.py (Add this file if it doesn't exist)

from django.contrib import admin
from .models import Item, Category

# Optional: Improve the Item view to show key information
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'is_available', 'seller', 'created_at')
    list_filter = ('category', 'is_available')
    search_fields = ('title', 'description')

# Register the models
admin.site.register(Item, ItemAdmin)
admin.site.register(Category)