from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Category

def home(request):
    """Главная страница"""
    return HttpResponse("""
    <h1>Добро пожаллоовать в наш магазин!</h1>
    <p>Это главная страница нашего интернет-магазина.</p>
    <a href="/products/">Посмотреть товары</a>
    """)

def product_list(request):
    """Список всех товаров"""
    products = Product.objects.filter(is_available=True)

    html = "<h1>Наши товары</h1><ul>"
    for product in products:
        html += f"<li>{product} руб.</li>"
    html += "</ul>"
    html += "<a href='/'>На главную</a>"
    return HttpResponse(html)

def category_products(request, category_id):
    """Товары определенной категории"""
    try:
        category = Category.objects.get(id=category_id)
        products = Product.objects.filter(category=category, is_available=True)

        html = f"<h1>Товары в категории {category}:</h1><ul>"
        for product in products:
            html += f"<li>{product} руб.</li>"
        html += "</ul>"
        html += "<a href='/products/'>Все товары</a> | "
        html += "<a href='/'>На главную</a>"
    except Category.DoesNotExist:
        html = "<h1>Категория не найдена</h1>"
    return HttpResponse(html)