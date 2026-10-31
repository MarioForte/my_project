from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    """Модель категории товара"""
    name = models.CharField(
        max_length=100,
        verbose_name="Название категории"
    )
    slug = models.SlugField(
        max_length=100, 
        blank=True,
        verbose_name="URL-имя"
    )
    # unique=True - желательно, но пропущен, чтобы не ломать миграцию с существующими данными
    description = models.TextField(
        blank=True,
        verbose_name="Описание"
    )
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель товара"""
    name = models.CharField(
        max_length=200,
        verbose_name="Название товара"
    )
    slug = models.SlugField(
        max_length=200,
        blank=True,
        verbose_name="URL-имя"
    )
    # unique=True - желательно, но пропущен, чтобы не ломать миграцию с существующими данными
    description = models.TextField(
        blank=True,
        verbose_name="Описание"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория"
    )
    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
        verbose_name="Изображение"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения"
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name="Доступен для продажи"
    )
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name}  - {self.price}"

class Order(models.Model):
    """Модель заказа"""
    STATUS_CHOICES = [
        ("pending", "Ожидает обработки"),
        ("processing", "В обработке"),
        ("shipped", "Отправлен"),
        ("delivered", "Доставлен"),
        ("cancelled", "Отменен"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                             related_name="orders", verbose_name="Пользователь")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    email = models.EmailField(verbose_name="Email")
    address = models.TextField(verbose_name="Адрес доставки")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, 
                              default="pending", verbose_name="Статус")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, 
                                      default=0, verbose_name="Общая стоимость")
    notes = models.TextField(blank=True, verbose_name="Примечания к заказу")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ №{self.id} - {self.user.username}"

class OrderItem(models.Model):
    """Модель позиции заказа"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, 
                              related_name="items", verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, 
                                verbose_name="Цена за единицу")
    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def get_total_price(self):
        """Общая стоимость позиции"""
        return self.quantity * self.price