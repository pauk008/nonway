from django.urls import path
from dashboard.views import add_to_cart
from .views import *  # Hamma funksiyalar, shu jumladan user_cabinet ham shu yerda import bo'ladi

urlpatterns = [
    path('', index, name="index"),
    path('home_page/', home_page, name="home_page"),
    path('order_page/', order_page, name="order_page"),
    path('order/', main_order, name="main_order"),

    # Sinxron yo'laklar
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),

    # AJAX yo'laklar
    path('add-to-cart-ajax/<int:product_id>/', add_to_cart_ajax, name='add_to_cart_ajax'),
    path('remove-from-cart-ajax/<int:product_id>/', remove_from_cart_ajax, name='remove_from_cart_ajax'),

    # 🔥 TO'G'RILANGAN JOYI: views. olib tashlandi, chunki tepada * bilan import qilingan
    path('cabinet/', user_cabinet, name='user_cabinet'),
]