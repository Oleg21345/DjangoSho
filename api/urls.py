from api.products.category_api import  *
from api.products.products_api import *
from api.users_reviews.reviews_api import *
from api.users_reviews.users_api import *
from api.apishopping.customer_api import *
from api.apishopping.order_api import *
from api.apishopping.order_product_api import *
from api.products.favourite_api import FavouriteProductAPI
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


urlpatterns = [
    # API settings
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),


    # Category API
    path("categories/", CategoryAPI.as_view(), name="categories_api"),
    path("categories/add", CategoryCreateAPI.as_view(), name="categories_add"),
    path("categories/<int:pk>/products/", ProductCategoryAPI.as_view(), name="category_products"),
    # Product API
    path("products/", ProductAPI.as_view(), name="product_api"),
    path("products/<int:pk>/", ProductOneAPI.as_view(), name="product_get_one"),
    path("products/add", ProductCreateAPI.as_view(), name="products_api_add"),
    path("products/<int:pk>/update/", ProductUpdateAPI.as_view(), name="product_update"),
    path("products/<int:pk>/destroy/", ProductDeleteAPI.as_view(), name="product_distroy"),
    # Galery API
    path("galery/", GaleryCreateAPI.as_view(), name="galery"),
    # Favourite API
    path("favourite/", FavouriteProductAPI.as_view(), name="favourite"),
    # Reviews API
    path("reviews/", ReviewsProductAPI.as_view(), name="reviews"),
    path("reviews/create", ReviewsCreateProductAPI.as_view(), name="reviews"),
    # User API
    path("users/", UserAPI.as_view(), name="users"),

    # Customer API
    path("customer", CustomerListCreateAPI.as_view(), name="customers_list_create"),
    path("customer/<int:pk>/", CustomerDetailAPI.as_view(), name="customer_detail"),

    # Order API
    path("order/", OrderListCreateAPI.as_view(), name="order"),

    # OrderProduct API
    path("order_product/", OrderProductListCreateAPI.as_view(), name="order_product"),
]



