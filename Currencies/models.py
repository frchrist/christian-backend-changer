from django.db import models

# Create your models here.

"""
Ce Model permet d'enregsitrer les monnaies et cripto-monnaie disponible  sur notre site web
"""
class Currencies(models.Model):
    name = models.CharField(max_length=20)
    code  = models.CharField(max_length=9)
    sell_value = models.DecimalField(decimal_places=4, max_digits=6)
    buy_value = models.DecimalField(decimal_places=4, max_digits=6)
    in_stock = models.PositiveIntegerField()
    min_qte = models.DecimalField(decimal_places=2,max_digits=6) 
    is_favorite = models.BooleanField(default=False)
    address_pattern = models.CharField(max_length=200)

    def __str__(self):
        return self.code

    @property
    def is_favorite(self):
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
