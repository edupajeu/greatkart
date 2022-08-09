from django.contrib import admin
from .models import Category


# Registered my models here.
class CategoryAdmin(admin.ModelAdmin):
    # Assigning auto complete from Category Name to Slug
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')

# Register in the Django admin
admin.site.register(Category, CategoryAdmin)
