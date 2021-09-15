import re
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_address(currencie_instance, address, case="serialization"):
   regex = currencie_instance.address_pattern
   pattern = re.compile(regex)
   if pattern.match(address):
       return True
   raise ValidationError(_("Your address is not valid"),400)


def validate_amount(instance,amount, case="ser"):
   min_ = instance.min_qte
   max_ = instance.in_stock
   if float(amount) > float(max_):
      raise ValidationError(_("Please your amount is too high"))
   if float(amount) < float(min_):
      raise ValidationError(_("Please your amount is to low"))
   return None
