from django.urls import path
from .views import * # Bu yerda hamma viewlar, jumladan api_send_sms va api_verify_sms ham avtomatik import bo'ladi

urlpatterns = [
    # Dashboardning o'zining mavjud yo'llari...
    path('', main_dashboard, name="main_dashboard"),

    # Savatga qo'shish yo'li:
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),

    # 🛠️ FRONTEND SO'ROVIGA MOSLAB O'ZGARTIRILGAN YO'LLAR (404 xatoni yo'qotadi):
    path('sms-auth/send-sms/', api_send_sms, name='api_send_sms'),
    path('sms-auth/verify-sms/', api_verify_sms, name='api_verify_sms'),

    # Qolgan product/list, category/list kabi yo'llar...
]