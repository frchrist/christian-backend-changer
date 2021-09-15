from django.contrib import admin
from django.contrib.auth.models import User
from .models import Client, ClientVerificationCode, ClientLoginCode

admin.site.register(Client)
admin.site.register(ClientVerificationCode)
admin.site.register(ClientLoginCode)

# Register your models here.
