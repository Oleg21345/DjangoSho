from shop.models import Reviews
from rest_framework import serializers
from rest_framework.generics import ListAPIView, CreateAPIView


class ReviewsySerializers(serializers.ModelSerializer):

    class Meta:
        model = Reviews
        fields = ("text", "author", "product", "rating", "create_at")

class ReviewsyAddSerializers(serializers.ModelSerializer):

    class Meta:
        model = Reviews
        fields = ("text", "author", "product", "rating")


class ReviewsProductAPI(ListAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsySerializers


class ReviewsCreateProductAPI(CreateAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsyAddSerializers







