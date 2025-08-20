from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils import timezone
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
from .models import Product, Category, Cart, CartItem, Order, OrderItem, Review
from .forms import CustomLoginForm, CustomSignupForm, ReviewForm
from django.shortcuts import render
from .models import Product
from django.shortcuts import redirect, render, get_object_or_404
from .models import Product
import openpyxl
from django.shortcuts import render, redirect
from .forms import ExcelUploadForm
from .models import Product, Category, Brand
from .models import UserProfile
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .forms import AddressForm
from .models import Address, City, Region
from django.views.decorators.http import require_POST

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Address
from .forms import AddressForm


@login_required
def manage_addresses(request):
    user = request.user  
    addresses = Address.objects.filter(user=user).order_by('-is_default', '-created_at')

    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            addr = form.save(commit=False)
            addr.user = user

            addr.first_name = getattr(user, 'first_name', '') or ''
            addr.last_name = getattr(user, 'last_name', '') or ''

            
            phone = ''
            try:
                phone = user.profile.phone_number or ''
            except Exception:
                phone = ''
            addr.phone_number = phone

           
            if not addresses.exists():
                addr.is_default = True

            addr.save()
            return redirect('manage_addresses')
    else:
        form = AddressForm()

    return render(request, 'products/manage_addresses.html', {
        'addresses': addresses,
        'form': form
    })


@login_required
@require_POST
def set_default_address(request, address_id):
    addr = get_object_or_404(Address, id=address_id, user=request.user)

    Address.objects.filter(user=request.user, is_default=True).update(is_default=False)

    addr.is_default = True
    addr.save()
    return redirect('manage_addresses')


@login_required
@require_POST
def delete_address(request, address_id):
    addr = get_object_or_404(Address, id=address_id, user=request.user)
    was_default = addr.is_default
    addr.delete()

  
    if was_default:
        other = Address.objects.filter(user=request.user).first()
        if other:
            other.is_default = True
            other.save()

    return redirect('manage_addresses')


@login_required
def get_cities(request, region_id):
   
    cities = City.objects.filter(region_id=region_id).order_by('name').values('id','name')
    return JsonResponse(list(cities), safe=False)


def import_products(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.active

            for row in sheet.iter_rows(min_row=2, values_only=True):
                name, description, category_name, brand_name, price, quantity, is_featured_val, is_popular_val = row

                category, _ = Category.objects.get_or_create(name=category_name)
                brand, _ = Brand.objects.get_or_create(name=brand_name)

                Product.objects.create(
                    name=name,
                    description=description,
                    category=category,
                    brand=brand,
                    price=price,
                    quantity=quantity,
                    is_featured=bool(is_featured_val),
                    is_popular=bool(is_popular_val)
                )
            messages.success(request, "Products imported successfully!")
            return redirect('shop')
    else:
        form = ExcelUploadForm()

    return render(request, 'products/import_products.html', {'form': form})


def search_results(request):
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query) if query else []

    if len(products) == 1:
        return redirect('product_detail', product_id=products[0].id)

    return render(request, 'products/search_results.html', {
        'results': products,
        'query': query
    })


def categories_processor(request):
    categories = Category.objects.all()
    return {'categories': categories}


from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import CustomLoginForm
from .models import UserProfile

def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
        if user.is_staff==True:
            return redirect('admin_dashboard')
        else:
            return redirect('home')
    else:
        form = CustomLoginForm()
        
    return render(request, 'products/registration/login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activation_link = request.build_absolute_uri(
                reverse('activate', kwargs={'uidb64': uid, 'token': token})
            )

            subject = "Activate your EchoStore account"
            message = render_to_string('products/email/activation_email.html', {
                'user': user,
                'activation_link': activation_link,
            })

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            messages.success(request, 'Please check your email to activate your account.')
            return redirect('login')
    else:
        form = CustomSignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate_account(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Account activated! You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid or expired activation link.')
        return redirect('signup')


@login_required
def profile_view(request):
    return render(request, 'products/profile.html')


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'products/my_orders.html', {'orders': orders})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'products/order_history.html', {'orders': orders})



@staff_member_required
def all_orders(request):
    orders = Order.objects.prefetch_related('orderitem_set__product').order_by('-created_at')
    return render(request, 'products/all_orders.html', {'orders': orders})


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def admin_dashboard(request):
    reviews = Review.objects.select_related('user', 'product').order_by('-created_at')
    return render(request, 'products/admin_dashboard.html', {'reviews': reviews})



def home(request):
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        products = Product.objects.all().order_by('price')
    elif sort == 'price_desc':
        products = Product.objects.all().order_by('-price')
    else:
        products = Product.objects.all()
    return render(request, 'products/home.html', {'products': products})


def all_products(request):
    products = Product.objects.all()
    return render(request, 'products/all_products.html', {'products': products})


def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'products/category_products.html', {
        'category': category,
        'products': products
    })


from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, OrderItem
from .forms import ReviewForm

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all().order_by('-created_at')

    has_ordered = False
    can_review = False
    has_reviewed = False

    if request.user.is_authenticated:
        has_ordered = OrderItem.objects.filter(order__user=request.user, product=product).exists()
        has_reviewed = product.reviews.filter(user=request.user).exists()
        can_review = has_ordered and not has_reviewed

        if request.method == 'POST' and can_review:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.product = product
                review.save()
                messages.success(request, 'Review submitted successfully!')
                return redirect('product_detail', product_id=product.id)
        else:
            form = ReviewForm()
    else:
        form = None

    
    average_rating = product.average_rating()
    total_reviews = product.total_reviews()

    return render(request, 'products/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
        'can_review': can_review,
        'average_rating': average_rating,
        'total_reviews': total_reviews,
        'rating_breakdown': product.rating_breakdown(),
    })



@login_required
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    for item in cart_items:
        item.item_total = item.product.price * item.quantity

    total = sum(item.item_total for item in cart_items)
    return render(request, 'products/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.quantity <= 0:
        messages.error(request, f"Sorry, '{product.name}' is out of stock.")
        return redirect('product_detail', product_id=product.id)

    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if created:
        cart_item.quantity = 1
        cart_item.save()
        messages.success(request, f"'{product.name}' added to cart.")
    else:
        if cart_item.quantity < product.quantity:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f"'{product.name}' quantity updated in cart.")
        else:
            messages.warning(request, f"You already have all available '{product.name}' in your cart.")

    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart')


@login_required
def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.quantity += 1
    item.save()
    return redirect('cart')


@login_required
def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('cart')


# =================== CHECKOUT ===================
@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    if request.method == 'POST':
        if not items.exists():
            messages.error(request, 'Your cart is empty.')
            return redirect('cart')

        # Check for sufficient stock
        for item in items:
            if item.product.quantity < item.quantity:
                messages.error(request, f"'{item.product.name}' has insufficient stock.")
                return redirect('cart')

        # Create the order
        total_price = sum(item.product.price * item.quantity for item in items)
        order = Order.objects.create(user=request.user, total_price=total_price, created_at=timezone.now())

        for item in items:
            # Reduce stock
            product = item.product
            product.quantity -= item.quantity
            product.save()

            # Create OrderItem
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item.quantity,
                price=product.price
            )

        # Clear cart
        items.delete()
        messages.success(request, 'Order placed successfully!')
        return redirect('checkout_success', order_id=order.id)

    # GET request - show checkout page
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, 'products/checkout.html', {
        'items': items,
        'total': total
    })


@login_required
def checkout_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'products/checkout_success.html', {
        'order': order,
        'order_items': order_items
    })
from django.shortcuts import render
from .models import Product

def shop(request):
    products = Product.objects.all()
    return render(request, 'products/shop.html', {'products': products})
