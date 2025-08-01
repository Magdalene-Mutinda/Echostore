from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category, Review, Cart, CartItem, Order, OrderItem, Brand

# Inline product form inside Category admin
class ProductInline(admin.TabularInline):
    model = Product
    extra = 5

# Category Admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag')
    inlines = [ProductInline]

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" />', obj.image.url)
        return "No Image"
    image_tag.short_description = 'Image'

# Product Admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_featured')
    list_filter = ('category', 'is_featured')
    search_fields = ('name',)
    list_editable = ('is_featured',)
    # Removed ProductImageInline inlines

# Brand Admin
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Register all models (removed ProductImage)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
