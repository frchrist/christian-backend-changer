from rest_framework import serializers
from .models import Currencies


class CurrencieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currencies
        fields = ["code", "name", "in_stock", "buy_value", "sell_value", "is_favorite","address_pattern", "min_qte"]
