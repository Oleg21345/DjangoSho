import datetime
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from shop.models import Category, Product, Reviews
from shop.forms import ProductForm
from django.db.models import Q, F
from shop.forms import ReviewForm, GaleryFormSet, CategoryForm
from django.contrib import messages
from django.shortcuts import redirect, render
from django.db.models import Avg
from django.urls import reverse_lazy


class Home(ListView):
    """Головна сторінка"""
    model = Product
    context_object_name = "prod"
    extra_context = {"title": "Головна сторінка"}
    template_name = "shop/index.html"

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return render(self.request, "shop/components/_products.html", context)
        return super().render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        """Додаткові параметри у шаблон"""
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(parent=None)[:4]

        return context


class AddProduct(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "shop/add_product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = GaleryFormSet(self.request.POST, self.request.FILES)
        else:
            context['formset'] = GaleryFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        else:
            return self.form_invalid(form)

        return redirect('home')


class DeleteProduct(DeleteView):
    model = Product
    context_object_name = "product"
    template_name = "shop/product_confirm_delete.html"
    extra_context = {"title": "Видалення товару"}
    success_url = reverse_lazy("home")


class UpdateProduct(UpdateView):
    """Оновлювати пости"""
    model = Product
    form_class = ProductForm
    template_name = "shop/add_product.html"
    extra_context = {"title": "Оновити інформацію про продукт"}

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse_lazy("home")


class AddCategory(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "shop/add_category.html"
    context_object_name = "category"
    success_url = reverse_lazy("add_product")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Додати категорію"
        return context


class SubCategory(ListView):
    """Показується які пости є в категорії та її підкатегорії"""
    paginate_by = 1

    model = Product
    context_object_name = "products"
    template_name = "shop/category_page.html"

    def get_queryset(self):
        parent_category = Category.objects.get(slug=self.kwargs["slug"])
        subcategories = parent_category.subcategories.all()

        products = Product.objects.filter(
            Q(category=parent_category) | Q(category__in=subcategories)
        ).order_by("create_at")

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










