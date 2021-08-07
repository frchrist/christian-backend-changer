from rest_framework import serializers
from .models import Currencies


class Currencies_Ser(serializers.ModelSerializer):
    class Meta:
        model = Currencies
        fields = "__all__"
