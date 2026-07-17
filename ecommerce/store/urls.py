from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [

    # 🏠 Home
    path('', views.home, name='home'),

    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # 🛍️ Cart
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/increase/<int:cart_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:cart_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('cart/remove/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),

    # 🧾 Checkout / Order
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('orders/', views.order_history, name='order_history'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),

    # 👤 Authentication
    path('register/', views.register, name='register'),

    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
   # path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('logout/', LogoutView.as_view(), name='logout'),

    

]