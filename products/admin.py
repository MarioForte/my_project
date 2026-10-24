from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    list_filter = ('name',)
    search_fields = ('name', "description")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        'category',
        'price',
        'is_available',
        'created_at'
    )
    list_filter = ('category', 'is_available', "created_at")
    search_fields = ('name', 'description')
    list_editable = ('price', 'is_available')
    readonly_fields = ('created_at', "updated_at")

    fieldsets = (
        ('Основная информация', {
            'fields': ("name", "description", "category")
        }),
        ("Цена и доступность", {
            'fields': ('price', "is_available")
        }),
        ("Изображение", {
            'fields': ('image',)
        }),
        ("Даты", {
            'fields': ('created_at', "updated_at"),
            'classes': ("collapse",)
        }),
    )
