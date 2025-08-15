from django import template
from shop.models import Product, Favourite
from django.db.models import Avg

register = template.Library()


@register.simple_tag(takes_context=True)
def get_sorted_products(context):
    request = context['request']
    sort = request.GET.get("sort", "all")

    queryset = Product.objects.all()

    if sort == "product_rating":
        queryset = queryset.annotate(avg_rating=Avg('reviews__rating')).order_by('avg_rating')
    else:
        options = {
            "all": None,
            "price": "-price",
            "watched": "-watched",
            "create_at": "-create_at",
            "title": "title",
            "title_minus": "-title",
            "product_rating": "-product.reviews"
        }

        order = options.get(sort)


        if order:
            queryset = queryset.order_by(order)
        else:
            queryset = queryset.order_by("?")

    return queryset[:4]


@register.simple_tag()
def get_favourite_product(user):
    fav_product = Favourite.objects.filter(user=user)
    products = [i.product for i in fav_product]
    return products
