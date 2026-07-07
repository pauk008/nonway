from django.shortcuts import render, redirect, get_object_or_404
from food.models import * # Barcha modellarni import qilish
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random
from . import forms
from . import services


# =========================================================
# 🚀 SMS API YO'LLARI (Dashboard uchun)
# =========================================================

@csrf_exempt
def api_send_sms(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            phone_number = data.get('phone_number')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Noto\'g\'ri ma\'lumot turi'}, status=400)

        if not phone_number:
            return JsonResponse({'error': 'Telefon raqam yuborilmadi!'}, status=400)

        sms_code = str(random.randint(1000, 9999))
        print("\n" + "=" * 50)
        print(f"🔥 [SMS KOD] {phone_number} uchun tasdiqlash kodi: {sms_code}")
        print("=" * 50 + "\n")

        request.session['sms_code'] = sms_code
        request.session['phone_number'] = phone_number
        return JsonResponse({'message': 'Kod muvaffaqiyatli yuborildi!'}, status=200)
    return JsonResponse({'error': 'Faqat POST so\'rov qabul qilinadi'}, status=405)


@csrf_exempt
def api_verify_sms(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_code = data.get('code')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Noto\'g\'ri ma\'lumot turi'}, status=400)

        saved_code = request.session.get('sms_code')
        phone_number = request.session.get('phone_number')

        if user_code and user_code == saved_code:
            # Sening Customer modelingga moslab phone_number qilindi uka
            customer, created = Customer.objects.get_or_create(
                phone_number=phone_number,
                defaults={'first_name': f"Mijoz_{phone_number[-4:]}"}
            )

            from django.contrib.auth.models import User
            user, u_created = User.objects.get_or_create(username=phone_number)
            login(request, user)

            return JsonResponse({'message': 'Tizimga muvaffaqiyatli kirdingiz!', 'redirect': '/'}, status=200)
        else:
            return JsonResponse({'error': 'Kiritilgan tasdiqlash kodi xato!'}, status=400)
    return JsonResponse({'error': 'Faqat POST so\'rov qabul qilinadi'}, status=405)


# =========================================================

def login_required_decarator(func):
    return login_required(func, login_url='login_page')


@login_required_decarator
def main_dashboard(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    customers = Customer.objects.all()
    orders = Order.objects.all()
    categories_products = []
    table_list = services.get_table()

    for category in categories:
        categories_products.append(
            {
                "category": category.title,
                "product": len(Product.objects.filter(category_id=category.id))
            }
        )

    ctx = {
        "counts": {
            "categories": len(categories),
            "products": len(products),
            "customers": len(customers),
            "orders": len(orders),
        },
        "categories_products": categories_products,
        "table_list": table_list,
    }
    return render(request, 'dashboard/index.html', ctx)


def login_page(request):
    if request.POST:
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main_dashboard')
    return render(request, 'dashboard/login.html')


@login_required_decarator
def logout_page(request):
    logout(request)
    return redirect('login_page')


# 🛠️ IMPORT ERROR YO'QOLISHI UCHUN ADD_TO_CART FUNKSIYASINI SHU YERGA HAM QO'SHIB QO'YDIK:
def add_to_cart(request, product_id):
    orders_list = request.COOKIES.get("orders")
    if orders_list:
        try:
            cart = json.loads(orders_list)
        except json.JSONDecodeError:
            cart = {}
    else:
        cart = {}

    p_id = str(product_id)

    if p_id in cart:
        action = request.GET.get('action')
        if action == 'minus':
            cart[p_id] -= 1
            if cart[p_id] <= 0:
                del cart[p_id]
        else:
            cart[p_id] += 1
    else:
        cart[p_id] = 1

    total_price = 0
    for key, val in cart.items():
        try:
            product = Product.objects.get(pk=int(key))
            total_price += product.price * val
        except Product.DoesNotExist:
            continue

    response = redirect(request.META.get('HTTP_REFERER', 'index'))
    response.set_cookie("orders", json.dumps(cart), max_age=3600 * 24 * 7)
    response.set_cookie("total_price", str(total_price), max_age=3600 * 24 * 7)
    return response