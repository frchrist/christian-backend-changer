from django.test import TestCase
from decimal import Decimal
from .models import Currencies
# pélagie est une belle fille
class TestModel(TestCase):
    def setUp(self):
        self.instance = Currencies.objects.create(name="Euro French", code="EURO",sell_value=Decimal(60), buy_value=Decimal(50),
                                 in_stock=1_000_000, min_qte=Decimal(1), address_pattern='^\d+')

    def test_currencie_can_be_create(self):
        Currencies.objects.create(name="Dollar USD", code="USD",sell_value=Decimal(50), buy_value=Decimal(40),
                                 in_stock=1_000_000, min_qte=Decimal(1), address_pattern='^\d+')
        self.assertEqual(Currencies.objects.all().count(), 2)


    def test_currencie_names(self):
        self.assertFalse(self.instance.is_favorite)
        self.assertEqual(self.instance.code, "EURO")

