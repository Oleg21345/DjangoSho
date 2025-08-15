import stripe
from django.shortcuts import render, redirect
from shop.forms import CustomerForm, ShippingForm
from shop.utils import CartForAuthUser, get_cart_data
from django.contrib import messages
from conf import settings
from shop.models import Customer
from django.urls import reverse

def cart(request):
    cart_info = get_cart_data(request)
    context = {
        "order": cart_info.get("order"),
        "order_products": cart_info.get("order_products"),
        "quantity": cart_info.get("quantity"),
        "title": "Корзина"
    }

    return render(request, "shop/cart.html", context)


def to_cart(request, product_id, action):
    if request.user.is_authenticated:
        CartForAuthUser(request, product_id, action)
        return redirect("cart")
    else:
        messages.error(request, "Ви маєте бути в системі щоб додати цей продукт")
        return redirect("login_register")


def checkout(request):
    """Сторінка оформлення замовлення"""
    cart_info = get_cart_data(request)
    context = {
        "order": cart_info.get("order"),
        "order_products": cart_info.get("order_products"),
        "quantity": cart_info.get("quantity"),
        "customerform": CustomerForm,
        "shippingform": ShippingForm,
        "title": "Оформлення замовлення"
    }
    return render(request, "shop/checkout.html", context)


def create_checkout_session(request):
    """Оплата stripe"""
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == "POST":
        user_cart = CartForAuthUser(request)
        cart_info = user_cart.get_cart_info()
        customer_form = CustomerForm(data=request.POST)
        shipping_form = ShippingForm(data=request.POST)
        if customer_form.is_valid() and shipping_form.is_valid():
            customer = Customer.objects.get(user=request.user)
            customer.first_name = customer_form.cleaned_data["first_name"]
            customer.last_name = customer_form.cleaned_data["last_name"]
            customer.gmail = customer_form.cleaned_data["gmail"]
            customer.phone_number = customer_form.cleaned_data["phone_number"]
            address = shipping_form.save(commit=False)
            address.customer = Customer.objects.get(user=request.user)
            address.order = user_cart.get_cart_info()["order"]
            customer.save()
            address.save()

        total_price = cart_info["price"]
        total_quantity = cart_info["quantity"]
        print(f"DEBUG total price {total_price}")
        print(f"DEBUG total price {total_quantity}")

        session = stripe.checkout.Session.create(
            line_items=[{
                "price_data": {"currency": "usd",
                               "product_data": {"name": "Товари з DjangoShop"},
                               "unit_amount": int(total_price * 100)},
                "quantity": total_quantity}],
            mode="payment",
            success_url=request.build_absolute_uri(reverse("success")),
            cancel_url=request.build_absolute_uri(reverse("success")),
        )
        return redirect(session.url, 303)


def success_payment(request):
    """Випадок коли оплата пройшла успішно"""
    user_cart = CartForAuthUser(request)
    user_cart.clear()
    messages.success(request, "Оплата пройшла успішно, дякую що ви з нами!")
    return render(request, "shop/success.html")










