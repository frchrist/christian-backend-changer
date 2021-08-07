from django.core.management.base import BaseCommand
from Authentication.models import Client
from faker import Faker
class Command(BaseCommand):
    help = "Create users"
    def handle(self, *args, **kwargs):
        fake = Faker()
        n = 20
        while n > 0:
            username = fake.first_name()
            email = fake.ascii_free_email()
            phone = fake.phone_number()
            password = fake.name()
            if(Client.objects.filter(email=email).exists() or Client.objects.filter(username=username).exists()):
                continue
            user = Client.objects.create_user(email=email, phone_number=phone, username=username)
            user.set_password(password)
            user.save()
            print("user %d - %s "%(n, username))
            n -= 1

