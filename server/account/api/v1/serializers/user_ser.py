from account.models import User, UserAddress
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = (
            "id",
            "main_address",
            "city",
            "state",
            "pin_code",
            "address_type",
            "updated_at",
        )