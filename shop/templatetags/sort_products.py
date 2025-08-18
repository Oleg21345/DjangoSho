from django import template
from shop.models import Product, Favourite, Order, OrderProduct
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

@register.filter
def page_range_sliding(current, total):
    current = int(current)
    total = int(total)

    pages = [1]

    start = max(current - 1, 2)
    end = min(current + 1, total - 1)

    pages.extend(range(start, end + 1))

    if total > 1:
        pages.append(total)

    return pages


@register.simple_tag(takes_context=True)
def favourite_category(context):
    request = context['request']
    if request.user.is_authenticated:
        return Favourite.objects.filter(user=request.user).count()
    return 0


@register.simple_tag(takes_context=True)
def order_product(context):
    request = context['request']
    if request.user.is_authenticated:
        return OrderProduct.objects.filter(order__customer__user=request.user).count()
    return 0
