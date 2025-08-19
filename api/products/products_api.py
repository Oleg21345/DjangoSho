from rest_framework import serializers
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from shop.models import Product, Galery


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "pk",
            "author",
            "title",
            "price",
            "quantity",
            "category",
            "desc",
            "info",
            "size",
            "color",
        )

class ProductAPI(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers


class ProductOneAPI(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers


class ProductCreateAPI(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

class ProductDeleteAPI(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

class ProductUpdateAPI(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers


class GalerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Galery
        fields = ("id", "product", "img")


class GaleryCreateAPI(CreateAPIView):
    """Створення картинки"""
    queryset = Galery.objects.all()
    serializer_class = GalerySerializer
    parser_classes = (MultiPartParser, FormParser)
