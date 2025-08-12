from django.views.generic import ListView
from shop.models import  Product,  Favourite
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin


class FavouriteDetail(LoginRequiredMixin ,ListView):
    model = Favourite
    context_object_name = "favourite"
    extra_context = {"title": "Сторінка обраного"}
    template_name = "shop/favourite.html"
    login_url = "login_register"

    def get_queryset(self):
        return Favourite.objects.filter(user=self.request.user).select_related('product')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        favourites = self.get_queryset()
        context['products'] = [fav.product for fav in favourites]
        return context


def favourite_product(request, product_slug):
    if request.user.is_authenticated:
        user = request.user
        product = Product.objects.get(slug=product_slug)
        favourite_products = Favourite.objects.filter(user=user)
        if product in [i.product for i in favourite_products]:
            fav_product = Favourite.objects.get(user=user, product=product)
            fav_product.delete()
        else:
            Favourite.objects.create(user=user, product=product)
        next_page = request.META.get("HTTP_REFERER", "category_detail")
        return redirect(next_page)
    else:
        return redirect("login_register")