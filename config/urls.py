"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

# 🚀 SMS API viewlarini bevosita shu yerda chaqirish uchun import qilamiz:
# (Agar views.py fayling dashboard ilovasida bo'lsa dashboard.views deb yoziladi,
#  agar food ilovasida bo'lsa food.views deb o'zgartir uka)
from dashboard.views import api_send_sms, api_verify_sms

# 1. JWT uchun kerakli view'larni import qilamiz
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # 💥 FRONTEND TO'G'RIdan-TO'G'RI SHU MANZILNI SO'RAYOTGANI UCHUN ENG TEPAGA QO'SHAMIZ:
    path('sms-auth/send-sms/', api_send_sms, name='api_send_sms'),
    path('sms-auth/verify-sms/', api_verify_sms, name='api_verify_sms'),

    # 2. DIQQAT: Bu yerda sening asosiy ilovang nonway ulab qo'yildi!
    path('', include("food.urls")),

    path('dashboard/', include("dashboard.urls")),

    # --- JWT AUTH API YO'LAKLARI ---
    # Maxway kabi login oynasi uchun token olish manzili:
    path('api/v1/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Token muddatini yangilash manzili:
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)