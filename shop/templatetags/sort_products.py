from django import template
from shop.models import Product

register = template.Library()


@register.simple_tag(takes_context=True)
def get_sorted_products(context):
    request = context['request']
    sort = request.GET.get("sort", "all")

    options = {
        "all": None,
        "price": "-price",
        "watched": "-watched",
        "create_at": "-create_at",
        "title": "title",
        "title_minus": "-title"
    }

    order = options.get(sort)

    queryset = Product.objects.all()

    if order:
        queryset = queryset.order_by(order)
    else:
        queryset = queryset.order_by("?")

    return queryset[:4]

