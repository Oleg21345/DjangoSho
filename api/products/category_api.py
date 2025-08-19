from shop.models import Category, Product
from rest_framework import serializers
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated


class CategorySerializers(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ("title", "img", "parent")

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CategoryProductSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ("id", "title", "img", "slug", "parent", "products")


class CategoryAPI(ListAPIView):
    """Видача всіх категорій"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializers


class ProductCategoryAPI(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Product.objects.none()

        category_id = self.kwargs["pk"]
        return Product.objects.filter(category_id=category_id)


class CategoryCreateAPI(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)












