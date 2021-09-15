from string import ascii_uppercase
from random import randrange, choices as Choices
from django.db import models
from Authentication.models import Client
from Currencies.models import Currencies
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
from django.utils import timezone

#exchange model
"""
ce model permet d'enregister  les echanges faitent par les clients

"""
class Exchange(models.Model):
    reference = models.CharField(_("reference"), max_length=20, blank=True, unique=True)
    currencie = models.ForeignKey(
                                  help_text=_("designant whether client currencie is"),
                                  to=Currencies,
                                  on_delete=models.CASCADE,
                                  related_name="currencie")
    devise = models.ForeignKey(
                               help_text=_("designante whether this currencie which client want to buy"),
                               to=Currencies,
                               on_delete=models.CASCADE,
                               related_name="devise")
    client = models.ForeignKey(to=Client, on_delete=models.PROTECT)
    state = models.CharField(_("transaction status"),
                                      help_text=_("Designante the status of current transaction"),
                                      choices=(("done","done"), ("pending", "pending"), ("failed", "failed")),
                                       max_length=9)
    to_wallet_address = models.CharField(_("reciever wallet address"),max_length=100)
    send_amount = models.DecimalField(_("send amount"), decimal_places=4, max_digits=15)
    recieve_amount = models.DecimalField(_("recieve amount"), decimal_places=4, max_digits=15, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "#REF %s %s - %s"%(self.reference,self.currencie, self.devise)
    @property
    def is_done(self):
        return self.state == "done"

    @property
    def status(self):
        return self.state
    @property
    def ref(self):
        return self.reference


@receiver(post_save,sender=Exchange)
def before_saving_exchange(sender, instance, created,*args,**kwargs):
    if created:
        instance.reference =  "%s-%d"%("".join(Choices(ascii_uppercase, k=2)),randrange(10000, 100000))
        instance.save()

class Withdraw(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(to=Client, on_delete=models.PROTECT)
    away = models.ForeignKey(to=Currencies, on_delete=models.PROTECT)
    address = models.CharField(_("reciever wallet address"),max_length=225)
    amount = models.DecimalField(_("send amount"), decimal_places=4, max_digits=15)
    recieve_amount = models.DecimalField(_("recieve amount"), decimal_places=4, max_digits=15, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s -%s"%(self.client.username, self.away.code, self.address)
