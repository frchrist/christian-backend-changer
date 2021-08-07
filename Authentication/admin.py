from django.contrib import admin
from django.contrib.auth.models import User
from .models import Client, ClientVerificationCode

admin.site.register(Client)
admin.site.register(ClientVerificationCode)

# Register your models here.
