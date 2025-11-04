from django.contrib import admin

# Register your models here.
# menu/admin.py
from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # list_display = ("name", "slug")l
    list_display = ("name", "name_ky", "name_en")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "name_ky", "name_en", "category", "price", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    fields = (
        "category",
        "is_active",
        "image",
        ("name", "name_ky", "name_en"),
        "price",
        "slug",
    )