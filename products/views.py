from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Product, Category, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .cart import Cart

def add_to_cart(request, product_id):
    """Добавление товара в корзину"""
    product = get_object_or_404(Product, id=product_id, is_available=True)
    cart = Cart(request)

    quantity = int(request.POST.get('quantity', 1))
    cart.add(product, quantity)

    messages.success(request, f"Товар {product.name} добавлен в корзину!")

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({
            'success': True,
            'cart_total_quantity': cart.get_total_quantity(),
            'message': f"Товар {product.name} добавлен в корзину!"
        })
    return redirect('product_list')

def remove_from_cart(request, product_id):
    """Удаление товара из корзины"""
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(product)
    messages.success(request, f"Товар {product.name} удален из корзины!")
    
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({
            'success': True,
            'cart_total_quantity': cart.get_total_quantity(),
            'message': f"Товар {product.name} удален из корзины!"
        })
    return redirect('cart_detail')

def update_cart_quantity(request, product_id):
    """обновление количества товара"""
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        cart = Cart(request)
        quantity = int(request.POST.get("quantity", 1))

        cart.update_quantity(product, quantity)
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            cart_total = cart.get_total_price()
            item_total = float(product.price) * quantity

            return JsonResponse({
                "success": True,
                "cart_total_quantity": cart.get_total_quantity(),
                "cart_total_price": cart_total,
                'item_total_price': item_total,
                "message": "Количество обновлено"
            })
    return redirect("cart_detail")

def cart_detail(request):
    """Детальная страница корзины"""
    cart = Cart(request)
    cart_items = cart.get_items()
    total_price = cart.get_total_price()

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        "cart_total_quantity": cart.get_total_quantity(),
    }
    return render(request, "products/cart_detail.html", context)

@login_required
def checkout(request):
    """Оформление заказа"""
    cart = Cart(request)
    cart_items = cart.get_items()

    if not cart_items:
        messages.warning(request, "Ваша корзина пуста!")
        return redirect('product_list')
    if request.method == "POST":
        order = Order.objects.create(
            user=request.user,
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
            email=request.POST.get("email"),
            address=request.POST.get("address"),
            total_price=cart.get_total_price(),
            notes=request.POST.get("notes", ''),
        )
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )
        cart.clear()
        messages.success(request, f"Заказ №{order.id} успешно оформлен!")
        return redirect('order_detail', order_id=order.id)
    inital_data = {}
    if request.user.is_authenticated:
        inital_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
    context = {
        'cart_items': cart_items,
        'total_price': cart.get_total_price(),
        'initial_data': inital_data
    }
    return render(request, 'products/checkout.html', context)

@login_required
def order_detail(request, order_id):
    """Детальная страница заказа"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        'order': order,
        'order_items': order.items.all()
    }
    return render(request, 'products/order_detail.html', context)

@login_required
def order_list(request):
    """Список заказов пользователя"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders
    }
    return render(request, "products/order_list.html", context)

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