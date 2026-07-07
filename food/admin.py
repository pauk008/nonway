from django.contrib import admin
from .models import Category, Product, Customer, Order, OrderProduct

# 1. Kategoriyalarni admin panelda ko'rsatish
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')
    list_display_links = ('id', 'title')
    search_fields = ('title',)

# 2. Mahsulotlarni chiroyli jadval qilish (name o'rniga title qo'yildi)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'cost', 'price', 'category', 'created_at')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description')
    list_filter = ('category', 'created_at')

# 3. Mijozlarni jadval ko'rinishida ko'rsatish
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'created_at')
    list_display_links = ('id', 'first_name', 'last_name')
    search_fields = ('first_name', 'last_name', 'phone_number')
    list_filter = ('created_at',)

# 4. Buyurtmalarni chiroyli qilish
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'payment_type', 'status', 'address', 'created_at')
    list_display_links = ('id', 'customer')
    list_filter = ('payment_type', 'status', 'created_at')
    search_fields = ('address',)

# 5. Savatdan buyurtmaga o'tgan nonlar ro'yxati
@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'count', 'price', 'created_at')
    list_display_links = ('id', 'order')
    list_filter = ('created_at',)