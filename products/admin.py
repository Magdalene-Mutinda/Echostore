from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category, Review, Cart, CartItem, Order, OrderItem, Brand

# --- Existing Admins ---
class ProductInline(admin.TabularInline):
    model = Product
    extra = 5

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag')
    inlines = [ProductInline]

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" />', obj.image.url)
        return "No Image"
    image_tag.short_description = 'Image'

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_featured')
    list_filter = ('category', 'is_featured')
    search_fields = ('name',)
    list_editable = ('is_featured',)

class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)

# ✅ --- FIXED: Custom Review Admin ---
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'display_star_rating', 'comment', 'created_at')

    @admin.display(description='Rating')
    def display_star_rating(self, obj):
        filled = '★' * obj.rating
        empty = '☆' * (5 - obj.rating)
        return format_html('<span style="color: orange;">{}{}</span>', filled, empty)

# --- Registering all Admins ---
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Review, ReviewAdmin)  # ✅ Use custom ReviewAdmin
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
