import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from .services import *
from config.settings import MEDIA_ROOT
from .forms import *

def home_page(request):
    if request.GET:
        product = get_product_by_id(request.GET.get("product_id", 0))
        return JsonResponse(product)

def order_page(request):
    if request.GET:
        user = get_user_by_phone(request.GET.get("phone_number", 0))
        return JsonResponse(user)

def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    orders = []
    orders_list = request.COOKIES.get("orders")

    if not orders_list or orders_list == "" or orders_list == "None":
        orders_list = "{}"

    total_price = 0
    try:
        cart_data = json.loads(orders_list)
    except:
        cart_data = {}

    if cart_data:
        for key, val in cart_data.items():
            try:
                product_obj = Product.objects.get(pk=int(key))
                orders.append({"product": product_obj, "count": val})
                total_price += product_obj.price * int(val)
            except Product.DoesNotExist:
                continue

    ctx = {
        'categories': categories,
        'products': products,
        'orders': cart_data,
        'orders_items': orders,
        'total_price': total_price,
        'MEDIA_ROOT': MEDIA_ROOT
    }

    response = render(request, 'food/index.html', ctx)
    response.set_cookie("total_price", str(total_price), max_age=3600 * 24 * 7, path="/")
    return response

def main_order(request):
    orders_list = request.COOKIES.get("orders")
    if not orders_list or orders_list == "" or orders_list == "None":
        orders_list = "{}"

    try:
        cart_data = json.loads(orders_list)
    except:
        cart_data = {}

    if request.POST:
        name_input = request.POST.get("name", "")
        phone_input = request.POST.get("phone_number", "")
        address_input = request.POST.get("address", "")

        full_name = name_input.split()
        first_name = full_name[0] if len(full_name) > 0 else "Mijoz"
        last_name = full_name[1] if len(full_name) > 1 else "Sotib oluvchi"

        customer, created = Customer.objects.get_or_create(
            phone_number=phone_input,
            defaults={'first_name': first_name, 'last_name': last_name}
        )

        order = Order.objects.create(customer=customer, address=address_input, payment_type=1)

        for key, value in cart_data.items():
            try:
                product_obj = Product.objects.get(pk=int(key))
                OrderProduct.objects.create(
                    count=int(value), price=product_obj.price,
                    product_id=product_obj.id, order_id=order.id
                )
            except Product.DoesNotExist:
                continue

        response = redirect("index")
        response.set_cookie("orders", "{}", max_age=3600 * 24 * 7, path="/")
        response.set_cookie("total_price", "0", max_age=3600 * 24 * 7, path="/")
        return response

    orders = []
    total_price = 0
    if cart_data:
        for key, val in cart_data.items():
            try:
                product_obj = Product.objects.get(pk=int(key))
                orders.append({"product": product_obj, "count": val})
                total_price += product_obj.price * int(val)
            except Product.DoesNotExist:
                continue

    ctx = {'orders_items': orders, 'total_price': total_price}
    return render(request, 'food/order.html', ctx)

def remove_from_cart(request, product_id):
    orders_list = request.COOKIES.get("orders")
    if not orders_list or orders_list == "" or orders_list == "None": orders_list = "{}"
    try: cart = json.loads(orders_list)
    except: cart = {}
    p_id = str(product_id)
    if p_id in cart:
        cart[p_id] -= 1
        if cart[p_id] <= 0: del cart[p_id]
    total_price = 0
    for key, val in cart.items():
        try:
            product = Product.objects.get(pk=int(key))
            total_price += product.price * int(val)
        except Product.DoesNotExist: continue
    response = redirect(request.META.get('HTTP_REFERER', 'index'))
    response.set_cookie("orders", json.dumps(cart), max_age=3600 * 24 * 7, path="/")
    response.set_cookie("total_price", str(total_price), max_age=3600 * 24 * 7, path="/")
    return response

def add_to_cart_ajax(request, product_id):
    orders_list = request.COOKIES.get("orders")
    if not orders_list or orders_list == "" or orders_list == "None": orders_list = "{}"
    try: cart = json.loads(orders_list)
    except: cart = {}
    p_id = str(product_id)
    cart[p_id] = cart.get(p_id, 0) + 1
    total_price = 0
    total_count = 0
    for key, val in cart.items():
        try:
            product = Product.objects.get(pk=int(key))
            total_price += product.price * int(val)
            total_count += int(val)
        except Product.DoesNotExist: continue
    response = JsonResponse({
        "status": "success",
        "total_price": f"{total_price:,}".replace(",", " ") + " so'm",
        "total_count": total_count
    })
    response.set_cookie("orders", json.dumps(cart), max_age=3600 * 24 * 7, path="/")
    response.set_cookie("total_price", str(total_price), max_age=3600 * 24 * 7, path="/")
    return response

def remove_from_cart_ajax(request, product_id):
    orders_list = request.COOKIES.get("orders")
    if not orders_list or orders_list == "" or orders_list == "None": orders_list = "{}"
    try: cart = json.loads(orders_list)
    except: cart = {}
    p_id = str(product_id)
    if p_id in cart:
        cart[p_id] -= 1
        if cart[p_id] <= 0: del cart[p_id]
    total_price = 0
    total_count = 0
    for key, val in cart.items():
        try:
            product = Product.objects.get(pk=int(key))
            total_price += product.price * int(val)
            total_count += int(val)
        except Product.DoesNotExist: continue
    formatted_price = f"{total_price:,}".replace(",", " ") + " so'm" if total_price > 0 else "Savat bo'sh"
    response = JsonResponse({
        "status": "success",
        "total_price": formatted_price,
        "total_count": total_count
    })
    response.set_cookie("orders", json.dumps(cart), max_age=3600 * 24 * 7, path="/")
    response.set_cookie("total_price", str(total_price), max_age=3600 * 24 * 7, path="/")
    return response


# Faylning eng tagiga qo'sh uka:

from django.contrib.auth.decorators import login_required

@login_required(login_url='index') # Agar login qilmagan bo'lsa, bosh sahifaga otib yuboradi
def user_cabinet(request):
    """ Tizimga kirgan mijozning shaxsiy kabineti """
    try:
        # Kirgan userning username'i (telefon raqami) orqali Customer profilini topamiz
        customer = Customer.objects.get(phone_number=request.user.username)
        # Faqat shu mijozga tegishli buyurtmalarni bazadan olamiz
        my_orders = Order.objects.filter(customer=customer).order_by('-id')
    except Customer.DoesNotExist:
        my_orders = []

    ctx = {
        'my_orders': my_orders,
    }
    return render(request, 'food/cabinet.html', ctx)