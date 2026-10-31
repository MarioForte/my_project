from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name="product_list"),
    path('category/<int:category_id>/', views.category_products, 
         name="category_products"),

    # Корзина
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', views.update_cart_quantity, name='update_cart_quantity'),

    # Заказы
    path('checkout/', views.checkout, name="checkout"),
    path('orders/', views.order_list, name="order_list"),
    path('orders/<int:order_id>/', views.order_detail, name="order_detail"),
]
