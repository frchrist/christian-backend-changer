from django.shortcuts import render
from .models import Currencies
from rest_framework import (mixins, viewsets)
from rest_framework.response import Response
from .serializers import Currencies_Ser

class ListCurrencies(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = Currencies_Ser
    queryset = Currencies.objects.all()



