from shop.models import OrderProduct
from rest_framework import serializers
from rest_framework.generics import ListCreateAPIView

class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = "__all__"

class OrderProductListCreateAPI(ListCreateAPIView):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer