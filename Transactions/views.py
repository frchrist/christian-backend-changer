from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner,HasVerifiedEmail
from .models import Exchange, Withdraw
from Currencies.models import Currencies
from .serializers import ReadTransactionSerializer, WriteTransactionSerializer,WithdrawSerializer

class TransactionViews(ModelViewSet):
    queryset = Exchange.objects.select_related("currencie", "devise", "client")
    permission_classes = (IsAuthenticated,)
    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadTransactionSerializer
        return WriteTransactionSerializer

    def get_queryset(self):
        return Exchange.objects.filter(client__id=self.request.user.id)

    def perform_create(self, serializer):
        send = serializer.validated_data["send_amount"]
        currencie = serializer.validated_data["currencie"]
        devise = serializer.validated_data["devise"]
        recieve = (float(currencie.sell_value)/float(devise.buy_value)) * float(send)
        serializer.save(client=self.request.user, recieve_amount=recieve, state="pending")
        print("sending request ....")

class WithdrawViews(ModelViewSet):
    queryset = Withdraw.objects.select_related("away", "client")
    permission_classes = [IsAuthenticated]
    serializer_class = WithdrawSerializer
    def get_queryset(self):
        return Withdraw.objects.filter(client__id=self.request.user.id)
    def perform_create(self, serializer):
        amount = serializer.validated_data.get("amount")
        ltc_instance = Currencies.objects.get(code="LTC")
        away = serializer.validated_data.get("away")
        recieve = (float(ltc_instance.sell_value)/float(away.buy_value)) * float(amount)
        serializer.save(client=self.request.user, recieve_amount=recieve)
