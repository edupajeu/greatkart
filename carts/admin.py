from django.contrib import admin
from .models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')  # It shows in a tidy way at the Django admin


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'is_active')


# It should be two registration for each item in the Django admin
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
