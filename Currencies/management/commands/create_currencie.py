from django.core.management.base import BaseCommand
from Currencies.models import Currencies
from faker import Faker
import random
from decimal import Decimal

class Command(BaseCommand):
    help = "Create Fake currencies just for testing"

    def handle(self, *args, **kwargs):
        fake = Faker()
        count = 10
        while count > 0:
            code, name = fake.currency()
            buy = random.randint(Decimal(1), Decimal(100))
            sell = random.randint(Decimal(1), Decimal(100))
            in_stock = random.randint(1, 100)
            min_qte = random.randint(Decimal(1), Decimal(10))
            pattern = "[a-zA-Z0-9]"
            if Currencies.objects.filter(code=code).exists():
                continue
            c = Currencies.objects.create(name=name, code=code, sell_value=sell, buy_value=buy, in_stock=in_stock, min_qte=min_qte, address_pattern=pattern)
            c.save()
            print("%s was created"%c.name)
            count -= 1

