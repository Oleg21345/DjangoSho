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