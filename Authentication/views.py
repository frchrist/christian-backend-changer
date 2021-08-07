from rest_framework import (mixins, viewsets)
import random
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import Auth_serializer
from .models import Client , ClientVerificationCode
"""
author : christi@n
date  :  06/08/2021
API for crypto currency exchange
"""

class VerifiedClient(APIView):
    def post(self, request):
        user_code = request.data.get("code", "")
        try:
            VcodeInstance = ClientVerificationCode.objects.get(code=user_code)
            client = Client.objects.get(email=VcodeInstance.client.email)
            if VcodeInstance.is_valid:
                if not client.is_verified:
                    client.is_verified = True
                    client.save()
                VcodeInstance.delete()
                return Response({"Success":"Votre compte à été bien activé"})
            else:
                VcodeInstance.delete()
                newVcodeInstance = ClientVerificationCode.objects.create(code=random.randrange(1000, 10000), client=client)
                newVcodeInstance.save()
                return Response({'Error':"Ce code est expiré, verifier votre boite de messagerie et reéssayé"}, status=400)
        except Exception as e:
            print(e)
            return Response({"Error":"Code invalide"}, status=400)

class ListClient(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = Auth_serializer
    queryset = Client.objects.all()

class AddClient(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = Auth_serializer
    querset = Client.objects.all()

class ListSubUser(APIView):
    def get(self, request, *args, **kwargs):
        query = Client.objects.filter(sponsor_id=kwargs["pk"])
        serializer = Auth_serializer(query, many=True)

        print(request.user)
        return Response(serializer.data, status=200)
