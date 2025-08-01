from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'), 
    path('accounts/', include('django.contrib.auth.urls')),  # Login,
    path('', include('products.urls')),
    path('cart/',views.view_cart, name='cart'),
    path('cart/increase/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)