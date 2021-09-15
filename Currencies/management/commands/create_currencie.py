from django.core.management.base import BaseCommand
from Currencies.models import Currencies

currencies =[ {
        "name":"BitCoin",
        "code":"BTC",
        "sell_value":36_000_430,
        "buy_value":"36_000_000",
        "in_stock":4,
        "min_qte":0.0002,
        "is_favorite":True,
        "address_pattern":"^3[a-zA-Z0-9]{33}$"
    },
             {
        "name":"Litcoin",
        "code":"LTC",
        "sell_value":174,
        "buy_value":"170.2",
        "in_stock":120,
        "min_qte":0.002,
        "is_favorite":True,
        "address_pattern":"^M[a-zA-Z0-9]{33}$"
             }
]

class Command(BaseCommand):
    help = "Create Fake currencies just for testing"

    def handle(self, *args, **kwargs):
        for item in currencies:
            Currencies.objects.create(**item)
