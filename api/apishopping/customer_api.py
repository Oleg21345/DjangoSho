from shop.models import Customer
from rest_framework import serializers
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

class CustomerListCreateAPI(ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerDetailAPI(RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
