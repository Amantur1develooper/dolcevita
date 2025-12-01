# core/admin.py
from django.contrib import admin
from core.models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    list_editable = ("order",)
    search_fields = ("name", "name_ky", "name_en")
    ordering = ("order", "name")

class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    fields = ("name", "price", "order", "is_active")
    ordering = ("order", "name")
    show_change_link = True

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "order", "is_active")
    list_filter = ("category", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("name", "name_ky", "name_en")
    ordering = ("category", "order", "name")
