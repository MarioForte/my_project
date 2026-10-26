from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product, Category

def home(request):
    """Главная страница"""
    popular_products = Product.objects.filter(is_available=True)[:4]
    context = {
        'popular_products': popular_products,
    }
    return render(request, 'home.html', context)

def product_list(request):
    """Список всех товаров"""
    products = Product.objects.filter(is_available=True)

    search_query = request.GET.get("q", '')
    if search_query:
        products = products.filter(name__icontains=search_query)

    sort = request.GET.get("sort", "-created_at")
    if sort in ['name', 'price', '-price', '-created_at']:
        products = products.order_by(sort)

    context = {
        'products': products,
    }
    return render(request, 'products/product_list.html', context)

def category_products(request, category_id):
    """Товары определенной категории"""
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category, is_available=True)

    context = {
        'products': products,
        "category": category
    }
    return render(request, "products/category_products.html", context)