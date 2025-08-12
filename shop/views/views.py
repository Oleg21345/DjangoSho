import datetime
from django.views.generic import ListView, DetailView
from shop.models import Category, Product, Reviews, Favourite
from django.db.models import Q, F
from shop.forms import ReviewForm
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Avg


class Home(ListView):
    """Головна сторінка"""
    model = Product
    context_object_name = "prod"
    extra_context = {"title": "Головна сторінка"}
    template_name = "shop/index.html"

    def get_context_data(self, **kwargs):
        """Додаткові параметри у шаблон"""
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(parent=None)
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['favourites_count'] = Favourite.objects.filter(user=self.request.user).count()
        else:
            context['favourites_count'] = 0
        return context


class SubCategory(ListView):
    """Показується які пости є в категорії та її підкатегорії"""

    model = Product
    context_object_name = "products"
    template_name = "shop/category_page.html"

    def get_queryset(self):
        parent_category = Category.objects.get(slug=self.kwargs["slug"])
        subcategories = parent_category.subcategories.all()

        products = Product.objects.filter(
            Q(category=parent_category) | Q(category__in=subcategories)
        ).order_by("?")

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        parent_categories = Category.objects.filter(parent=None)

        child_categories = Category.objects.exclude(parent=None)

        context["parent_categories"] = parent_categories
        context["child_categories"] = child_categories

        category_slug = self.kwargs.get("slug")
        if category_slug:
            try:
                selected_category = Category.objects.get(slug=category_slug)
                context["selected_category"] = selected_category
            except Category.DoesNotExist:
                context["selected_category"] = None
        else:
            context["selected_category"] = None

        return context


class ProductDetail(DetailView):
    """Детальніше про продукт"""

    model = Product
    context_object_name = "product"
    template_name = "shop/product_detail.html"


    def get_context_data(self, **kwargs):
        slug = self.kwargs["slug"]
        context = super().get_context_data(**kwargs)
        product = self.object

        parent_cat = product.category
        subcategory = parent_cat.subcategories.all()

        products = Product.objects.filter(
            Q(category=parent_cat) | Q(category__in=subcategory)
        ).exclude(id=product.id).order_by("?")

        context["products"] = products

        Product.objects.filter(slug=slug).update(watched=F("watched") + 1)
        product = Product.objects.get(slug=slug)
        context["avg_rating"] = product.reviews.aggregate(avg=Avg('rating'))['avg'] or 0

        if self.request.user.is_authenticated:
            context["review_form"] = ReviewForm()
            context["reviews"] = Reviews.objects.filter(product=product).order_by("-create_at")
        return context


    def get_queryset(self):
        return Product.objects.all()


def add_review(request, product_slug):
    """Додавання коментаря"""
    print("add_review called", request.POST)
    form = ReviewForm(data=request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.author = request.user
        product = Product.objects.get(slug=product_slug)
        review.product = product
        review.create_at = datetime.datetime.utcnow()
        review.save()
        message = "Ваш відгук був успішно залишений"
        messages.success(request, message, extra_tags='', fail_silently=False)
        return redirect("product_detail", slug=product_slug)
    else:
        form = ReviewForm()

    return redirect("product_detail", slug=product_slug)










