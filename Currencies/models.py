from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
"""
Ce Model permet d'enregsitrer les monnaies et cripto-monnaie disponible  sur notre site web
"""
class Currencies(models.Model):
    """
    The base currencie is fcfa
    """
    name = models.CharField(_("name"),
                            help_text=_('Designant the name of currencie'),
                            max_length=20, unique=True,
                            error_messages={
                                'unique':_("this name already exists")
                            }
                            )
    code  = models.CharField(_("code"),
                     help_text=_('Designant code of currencie'),
                             max_length=9,
                             unique=True,
                            error_messages={
                                'unique':_("this code  already exists")
                            }
                            )
    sell_value = models.DecimalField(_("sell value"),decimal_places=4, max_digits=15)
    buy_value = models.DecimalField(_('buy value'), decimal_places=4, max_digits=15)
    in_stock = models.PositiveIntegerField(_('max quantity'))
    min_qte = models.DecimalField(_('min quantity'), decimal_places=4,max_digits=15)
    is_favorite = models.BooleanField(_('favarite'), default=False)
    address_pattern = models.CharField(_("address pattern"),
                                       help_text=_("Designante regex of currencie address"),
                                       max_length=200)

    def __str__(self):
        return self.code

    @property
    def is_fav(self):
        return self.is_favorite
    @property
    def max_quantite(self):
        return self.instock

    @property
    def min_quatite(self):
        return self.min_qte
    class Mata:
        verbose_name_plural = "Currencies"
        ordering = ["code"]
