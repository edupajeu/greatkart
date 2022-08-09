from django.contrib import admin
from .models import Cart, CartItem

# Register in the Django admin
# It should be two registration for each item in the Django admin
admin.site.register(Cart)
admin.site.register(CartItem)
