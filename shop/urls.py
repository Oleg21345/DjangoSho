from django.urls import path
from shop.views.views import *
from shop.views.register_and_login import *

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("category/<slug:slug>/", SubCategory.as_view(), name="category_detail"),
    path("product/<slug:slug>/", ProductDetail.as_view(), name="product_detail"),
    path("login_register/", login_registration, name="login_register"),
    path("login_user/", user_login, name="login"),
    path("logout_user/", user_logout, name="logout"),
    path("register_user/", register_user, name="register")
]



