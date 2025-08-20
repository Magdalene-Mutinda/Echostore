from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg
from django.core.exceptions import ValidationError

def validate_excel_file(file):
    valid_extensions = ['xlsx', 'xls'] 
    ext = file.name.split('.')[-1].lower()  
    if ext not in valid_extensions:
        raise ValidationError('Only Excel files (.xlsx or .xls) are allowed.')


class Region(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class City(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="cities")
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.region.name})"

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    additional_phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField()
    additional_info = models.TextField(blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} — {self.address}"



def validate_image(file):
    valid_extensions = ['jpg', 'jpeg', 'png']
    ext = file.name.split('.')[-1].lower()
    if ext not in valid_extensions:
        raise ValidationError('Only JPG, JPEG, and PNG files are allowed.')


from django.utils.text import slugify
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

from django.db.models import Avg

class Product(models.Model):
    name = models.CharField(max_length=200)
    image1 = models.ImageField(upload_to='product_images/', validators=[validate_image], blank=True, null=True)
    image2 = models.ImageField(upload_to='product_images/', validators=[validate_image], blank=True, null=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    is_popular = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name

   
    def average_rating(self):
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg or 0, 1)

    
    def total_reviews(self):
        return self.reviews.count()

    
    def rating_breakdown(self):
        breakdown = {}
        total = self.reviews.count()
        for i in range(5, 0, -1): 
            count = self.reviews.filter(rating=i).count()
            percentage = (count / total * 100) if total > 0 else 0
            breakdown[i] = {
                "count": count,
                "percentage": round(percentage)
            }
        return breakdown



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity} × {self.product.name}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Cart"

@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.rating}⭐"

from django.contrib import admin
from .models import Product, Review

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'short_comment', 'created_at')
    list_filter = ('rating', 'created_at', 'product')
    search_fields = ('product__name', 'user__username', 'comment')
    readonly_fields = ('created_at',)

    def short_comment(self, obj):
        return obj.comment[:50] + ('...' if len(obj.comment) > 50 else '')
    short_comment.short_description = 'Comment'

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'price', 'quantity', 'average_rating_display', 'total_reviews')
    
    def average_rating_display(self, obj):
        return obj.average_rating()
    average_rating_display.short_description = 'Avg Rating'

    def total_reviews(self, obj):
        return obj.total_reviews()
    total_reviews.short_description = 'Reviews Count'



