from shop.models import Favourite
from rest_framework import serializers
from rest_framework.generics import ListAPIView



class FavoutiteySerializers(serializers.ModelSerializer):

    class Meta:
        model = Favourite
        fields = ("user", "product")


class FavouriteProductAPI(ListAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavoutiteySerializers

















