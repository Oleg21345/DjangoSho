import uuid
from django.db import models
from django.db.models import CASCADE
from django.urls import reverse
from django.contrib.auth.models import User

def generate_random_slug():
    return uuid.uuid4().hex[:12]

class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name="ім'я категорії")
    img = models.ImageField(upload_to="categories/", null=True, blank=True, verbose_name="Картинка")
    slug = models.SlugField(unique=True, null=True, blank=True, default=generate_random_slug)
    parent = models.ForeignKey("self", on_delete=CASCADE, null=True, blank=True,
                               verbose_name="Категорія", related_name="subcategories")


    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})

    def get_parent_cat_photo(self):
        if self.img:
            return self.img.url
        else:
            return "https://via.placeholder.com/150x100.png?text=No+Image"

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"PK категорії = {self.pk} Назва категорії {self.title}"

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name="ім'я категорії")
    price = models.FloatField()
    create_at = models.DateTimeField(auto_created=True, verbose_name="Час створення")
    watched = models.IntegerField(default=0, verbose_name="Перегляди")
    quantity = models.IntegerField(default=0, verbose_name="Кількість товару на складі")
    desc = models.CharField(default="Тут скоро щось буде", verbose_name="Опис")
    info = models.CharField(default="Додаткова інформація про продукт", verbose_name="Додаткова інформація")
    category = models.ForeignKey(Category ,on_delete=CASCADE, verbose_name="Категорія", related_name="products")
    slug = models.SlugField(unique=True, null=True, blank=True, default=generate_random_slug)
    size = models.IntegerField(default=30, verbose_name="Розмір в мм")
    color = models.CharField(max_length=30, default="Срібло", verbose_name="Матеріал/Колір")


    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

    def get_first_photo(self):
        if self.images.first():
            return self.images.first().img.url
        else:
            return "Скоро тут буде фотографія"

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'PK product = {self.pk} title = {self.title}'


    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"


class Galery(models.Model):
    img = models.ImageField(upload_to="product/", null=True, blank=True, verbose_name="Картинка")
    product = models.ForeignKey(Product, on_delete=CASCADE, related_name="images")

    class Meta:
        verbose_name = "Картинка"
        verbose_name_plural = "Галерея картинок"


class Reviews(models.Model):
    text = models.TextField(verbose_name="Текст відгуку")
    author = models.ForeignKey(User, on_delete=CASCADE, verbose_name="Автор")
    product = models.ForeignKey(Product, on_delete=CASCADE, verbose_name="Продукт",  related_name="reviews")
    rating = models.PositiveSmallIntegerField(default=0)
    create_at = models.DateTimeField(auto_created=True, verbose_name="Час створення")

    def __str__(self):
        return self.author.username

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"


class Favourite(models.Model):
    """Обране користувачем"""
    user = models.ForeignKey(User, on_delete=CASCADE, verbose_name="Користувач")
    product = models.ForeignKey(Product, on_delete=CASCADE, verbose_name="Продукт")

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = "Обране"
        verbose_name_plural = "Обрані"

class Gmail(models.Model):
    gmail = models.EmailField(unique=True, verbose_name="Пошта")
    user = models.ForeignKey(User, on_delete=CASCADE, blank=True, null=True, verbose_name="Користувач")

    class Meta:
        verbose_name = "Пошта"
        verbose_name_plural = "Пошти"


class Customer(models.Model):
    user = models.OneToOneField(User, models.SET_NULL, blank=True, null=True, verbose_name="Користувач")
    first_name = models.CharField(max_length=255, verbose_name="Ім'я")
    last_name = models.CharField(max_length=255, verbose_name="Фамілія")
    gmail = models.EmailField(unique=True, verbose_name="Пошта")
    phone_number = models.CharField(max_length=255, verbose_name="Номер телефону")

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = "Замовник"
        verbose_name_plural = "Замовники"


class Order(models.Model):
    """Корзина"""
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True,
                                 verbose_name="Покупець")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Час створення")
    is_completed = models.BooleanField(default=False, verbose_name="Закінчене замовлення")
    shiping = models.BooleanField(default=True, verbose_name="Доставка")

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"

    @property
    def get_cart_total_price(self):
        """Тут йде рахунок суми товарів в корзині"""
        order_products = self.ordered.all()
        total_price = sum([product.get_total_price for product in order_products])
        return total_price

    @property
    def get_cart_total_quantity(self):
        order_products = self.ordered.all()
        total_quantity = sum([product.quantity for product in order_products])
        return total_quantity


class OrderProduct(models.Model):
    """Прив'язка продукту до корзини"""
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="Продукт")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name="ordered")
    quantity = models.IntegerField(default=0, null=True, blank=True) # Кількість товару
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Замовлення в корзині"
        verbose_name_plural = "Замовленн в корзині"

    @property
    def get_total_price(self):
        """ Тут йде рахунок кількості товару"""
        total_price = self.product.price * self.quantity
        return total_price


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    city = models.CharField(max_length=355, verbose_name="Місто")
    state = models.CharField(max_length=355, verbose_name="Район")
    street = models.CharField(max_length=355, verbose_name="Вулиця")
    create_at = models.DateTimeField(auto_created=True, verbose_name="Час створення")

    def __str__(self):
        return self.street

    class Meta:
        verbose_name = "Адреса"
        verbose_name_plural = "Адреса"




