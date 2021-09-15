from rest_framework import serializers
from .models import Exchange, Withdraw
from rest_framework.exceptions import ValidationError
from Currencies.serializers import CurrencieSerializer
from Authentication.models import Client
from Currencies.models import Currencies
from django.contrib import auth
from django.utils.translation import gettext_lazy as _
from .validators import validate_address, validate_amount
class WriteTransactionSerializer(serializers.ModelSerializer):

    currencie = serializers.SlugRelatedField(slug_field="code", queryset=Currencies.objects.all())
    devise = serializers.SlugRelatedField(slug_field="code", queryset=Currencies.objects.all())
    class Meta:
        model =Exchange
        fields = ["devise", "currencie", "to_wallet_address","send_amount"]

    def create(self, validated_data):

        client = validated_data.get("client", None)
        validate_address(validated_data.get("devise",None), validated_data.get("to_wallet_address"))
        validate_amount(validated_data.get("devise",None), validated_data.get("send_amount"))
        if client != None and client.email_is_valid:
            model = self.Meta.model(**validated_data)
            model.save()
            return model
        else:
            raise  ValidationError(_("Please before making any transaction, verified your email address"), code=400)

class ReadTransactionSerializer(serializers.ModelSerializer):

    currencie = CurrencieSerializer()
    devise = CurrencieSerializer()
    client = serializers.SlugRelatedField(slug_field="email", queryset=Client.objects.all())
    class Meta:
        model =Exchange
        fields = ["reference","devise", "date","client","currencie", "state", "to_wallet_address","send_amount", "recieve_amount"]
        read_only_fields = fields


class WithdrawSerializer(serializers.ModelSerializer):

    away = serializers.SlugRelatedField(slug_field="code", queryset=Currencies.objects.all())
    class Meta:
        model = Withdraw
        fields = ["amount","away","date", "address", "recieve_amount"]
        read_only_fields = ["date","recieve_amount"]


    def create(self, validated_data):
        validate_address(validated_data.get("away"), validated_data.get("address", None))
        if float(validated_data.get("client").balance < float(validated_data.get("amount"))):
            raise ValidationError(_("your balance is insuffisante"), 400)
        md = self.Meta.model(**validated_data)
        md.save()
        return md
