from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Auth
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Custom Login
    path('custom_login/', views.custom_login, name='custom_login'),

    # Products
    
    path('search/', views.search_results, name='search_results'),
    path('orders/', views.all_orders, name='all_orders'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('import-products/', views.import_products, name='import_products'),

    # Cart
    path('cart/', views.view_cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),

    # Checkout
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/success/<int:order_id>/', views.checkout_success, name='checkout_success'),
    path('profile/', views.profile_view, name='profile'),
    path('shop/',views.shop, name='shop'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('shop/', views.all_products, name='shop'),

    #address management
    path('my-addresses/', views.manage_addresses, name='manage_addresses'),
    path('set-default-address/<int:address_id>/', views.set_default_address, name='set_default_address'),
    path('delete-address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('ajax/get-cities/<int:region_id>/', views.get_cities, name='ajax_get_cities'),
]

