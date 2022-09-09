from django.contrib import admin
from .models import Product, Variation, ReviewRating


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')  # Display the names in a list
    list_editable = ('is_active',)  # It allows edit the field from a list
    list_filter = ('product', 'variation_category', 'variation_value', 'is_active')
    # It allows filter by those attributes


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)

