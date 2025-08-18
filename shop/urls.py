from django.urls import path
from shop.views.views import *
from shop.views.register_and_login import *
from shop.views.favourite_views import *
from shop.views.send_email_views import *
from shop.views.shopping_cart_views import *

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("category/<slug:slug>/", SubCategory.as_view(), name="category_detail"),
    path("product/<slug:slug>/", ProductDetail.as_view(), name="product_detail"),
    path("favourite/", FavouriteDetail.as_view(), name="favourite"),
    path("add_product/", AddProduct.as_view(), name="add_product"),
    path("history_buys", HistoryBuy.as_view(), name="history"),
    path("add_category/", AddCategory.as_view(), name="add_category"),

    # Функція
    path("add_gmail/", add_subs_gmail, name="add_gmail"),
    path("login_register/", login_registration, name="login_register"),
    path("login_user/", user_login, name="login"),
    path("logout_user/", user_logout, name="logout"),
    path("register_user/", register_user, name="register"),
    path("add_review/<slug:product_slug>/", add_review, name="add_review"),
    path("add_favourite/<slug:product_slug>/", favourite_product, name="add_fav"),
    path("send_email/", send_email_to_subs, name="send_email"),
    path("cart/", cart, name="cart"),
    path("to_cart/<int:product_id>/<str:action>/", to_cart, name="to_cart"),
    path("checkout/", checkout, name="checkout"),
    path("payment/", create_checkout_session, name="payment"),
    path("success/", success_payment, name="success"),
    path("coupon_using", coupon_using, name="coupon_using"),
    path("delete_product/<slug:slug>/", DeleteProduct.as_view(), name="delete_product"),
    path("update_product/<slug:slug>/", UpdateProduct.as_view(), name="update_product"),
]





