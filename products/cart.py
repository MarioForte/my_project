class Cart:
    """Класс для работы с корзиной в сессии"""
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        """Добавление товара в корзину"""
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price),
                'name': product.name,
                'image': product.image.url if product.image else '',
            }
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Сохранение корзины в сессии"""
        self.session.modified = True

    def remove(self, product):
        """Удаление товара из корзины"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update_quantity(self, product, quantity):
        """Обновление количества товара"""
        product_id = str(product.id)

        if product_id in self.cart:
            if quantity > 0:
                self.cart[product_id]['quantity'] = quantity
            else:
                self.remove(product)
            self.save()

    def clear(self):
        """Очистка корзины"""
        del self.session['cart']
        self.save()

    def get_total_price(self):
        """Общая стоимость корзины"""
        return sum(
            float(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def get_total_quantity(self):
        """Общее количество товаров в корзине"""
        return sum(
            item['quantity'] for item in self.cart.values()
        )

    def get_items(self):
        """Получение всех товаров в корзине"""
        product_ids = self.cart.keys()
        from .models import Product
        products = Product.objects.filter(id__in=product_ids)

        cart_items = []
        for product in products:
            item = self.cart[str(product.id)]
            cart_items.append({
                'product': product,
                'quantity': item['quantity'],
                'total_price': float(item['price']) * item['quantity'],
                'image_url': item.get('image', '')
            })
        return cart_items

    def __len__(self):
        """Количество позиций в корзине"""
        return len(self.cart)