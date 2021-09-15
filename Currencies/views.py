from django.shortcuts import render
from .models import Currencies
from rest_framework import (mixins, viewsets)
from rest_framework.response import Response
from .serializers import CurrencieSerializer

class ListCurrencies(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CurrencieSerializer
    queryset = Currencies.objects.all()



