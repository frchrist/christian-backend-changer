from django.test import TestCase
from decimal import Decimal
from Authentication.models import Client
from Currencies.models import Currencies
from .models import Exchange
# Create your tests here.


class TestModel(TestCase):
    def setUp(self):
        self.instance = Currencies.objects.create(name="Euro Pm", code="EPM",sell_value=Decimal(60), buy_value=Decimal(50),
                                 in_stock=1_000_000, min_qte=Decimal(1), address_pattern='^\d+')
        self.instance1 = Currencies.objects.create(name="Euro Peyeer", code="EP",sell_value=Decimal(60), buy_value=Decimal(50),
                                 in_stock=1_000_000, min_qte=Decimal(1), address_pattern='^\d+')

        self.client = Client.objects.create(username="username", password="password", email="email@gmail.com")

    def test_transaction_created(self):
         t = Exchange.objects.create(currencie=self.instance,
                                send_amount=10,
                                recieve_amount=11,
                                to_wallet_address="core-dore-core",
                                state="done",
                                devise=self.instance1,
                               client=self.client)

         self.assertIsNotNone(t.ref)
         self.assertIsInstance(t.ref, str, msg="The reference must be str")


