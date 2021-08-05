from django.db import models
from Authentication.models import Client
from Currencies.models import Currencies
# Create your models here.

#exchange model
"""
ce model permet d'enregister  les echanges faitent par les clients

"""
class Exchange(models.Model):
    currencie = models.ForeignKey(to=Currencies, on_delete=models.CASCADE)
    devise = models.ForeignKey(to=Currencies, on_delete=models.CASCADE)
    client = models.ForeignKey(to=Client, on_delete=models.PROTECT)
    state = models.CharField(choice=(("done","done"), ("pending", "pending")), max_length=9)
    to_wallet_address = models.CharField(max_length=100)
    send_amount = models.decimalField(decimal_places=4) 
    recieve_amount = models.decimalField(decimal_places=4) 

    def __str__(self):
        return "%s - %s"%(currencie, devise)
    @property
    def is_done(self):
        return self.state == "done"
