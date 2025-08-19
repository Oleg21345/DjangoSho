from shop.models import Order
from rest_framework import serializers
from rest_framework.generics import ListCreateAPIView


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

class OrderListCreateAPI(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer