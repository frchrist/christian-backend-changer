from django.core.management.base import BaseCommand
from Authentication.models import ClientVerificationCode, ClientLoginCode



class Command(BaseCommand):
    help = "delete all login and verification code who's are invalid"
    def handle(self,*args,**kwargs):


        for query in ClientVerificationCode.objects.all():
            if not query.is_valid:
                query.delete()
        for query in ClientLoginCode.objects.all():
            if not query.is_valid:
                query.delete()
