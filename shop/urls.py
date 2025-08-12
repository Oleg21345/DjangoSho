from django.urls import path
from shop.views.views import *
from shop.views.register_and_login import *
from shop.views.favourite_views import *
from shop.views.send_email_views import *

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("category/<slug:slug>/", SubCategory.as_view(), name="category_detail"),
    path("product/<slug:slug>/", ProductDetail.as_view(), name="product_detail"),
    path("favourite/", FavouriteDetail.as_view(), name="favourite"),
    path("add_gmail/", add_subs_gmail, name="add_gmail"),

    # Функція
    path("login_register/", login_registration, name="login_register"),
    path("login_user/", user_login, name="login"),
    path("logout_user/", user_logout, name="logout"),
    path("register_user/", register_user, name="register"),
    path("add_review/<slug:product_slug>/", add_review, name="add_review"),
    path("add_favourite/<slug:product_slug>/", favourite_product, name="add_fav"),
    path("send_email/", send_email_to_subs, name="send_email"),
]



