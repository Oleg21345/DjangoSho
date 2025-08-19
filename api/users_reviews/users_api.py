from rest_framework import serializers
from rest_framework.generics import ListAPIView
from django.contrib.auth.models import User



class UsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )


class UserAPI(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializers






