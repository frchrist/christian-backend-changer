from django.core.mail import send_mail
from .models import Client,ClientVerificationCode
from rest_framework import serializers


class Auth_serializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    class Meta:
        model = Client
        fields = ["id", "username",'email', "balance","phone_number","password",
                  "last_name","sponsor_id",
                  "is_verified","can_receive_notification","country" ]
        read_only_fields = ["id",  "balance", "is_verified", "can_receive_notification", "country"]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        client = Client.objects.create_user(**validated_data)
        client.set_password(validated_data["password"])
        client.save()


        #gestion des lien de parainnage.
        SID = validated_data["sponsor_id"]
        if(SID != None and Client.objects.filter(id=SID).exists()):
            s_client = Client.objects.get(id=SID)
            s_client.balance = s_client.get_balance + 10
            s_client.save()
        return client
