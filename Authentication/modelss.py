from django.db import models
from django.core.mail import send_mail
from random import randrange
from django.db.models.signals import post_save, pre_save
from django.utils import timezone
#from rest_framework.authtoken.models import Token
from django.conf import settings
from django.dispatch import receiver


# Create your models here.
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class ClientManager(BaseUserManager):
    def create_user(self, email,phone_number, username=None, first_name=None, last_name=None, password=None, sponsor=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
            sponsor =sponsor,
            username=username,
            last_name=last_name,
            first_name=first_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number,username, first_name=None, last_name=None, password=None):
        user = self.create_user(
            email,
            username=username,
            password=password,
            phone_number=phone_number
        )
        user.is_admin = True
        user.can_receive_notification = False
        user.balance = 0
        user.save(using=self._db)
        return user


class Client(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        verbose_name='Nom utilisateur',
        max_length=255,
        unique=True,
    )
    phone_number = models.CharField(
        verbose_name='Numero de telephone ',
        max_length=20,
    )
    first_name = models.CharField(
        verbose_name='Nom ',
        max_length=255,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        verbose_name=' Prénom ',
        max_length=255,
        blank=True,
        null=True,
    )
    sponsor = models.ForeignKey(to="self", on_delete=models.CASCADE, null=1, blank=1, default=None)

    is_active = models.BooleanField(default=True)

    is_admin = models.BooleanField(default=False)
    balance = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    can_receive_notification = models.BooleanField(default=False)
    country = models.CharField(default="togo", max_length=20)
    double_auth =  models.BooleanField(default=False)

    objects = ClientManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['phone_number',"username" ]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True


    def has_module_perms(self, app_label):
        return True

    @property
    def get_balance(self):
        return self.balance
    @property
    def is_valid(self):
        return self.is_verified

    @property
    def can_be_notify(self):
        return self.can_receive_notification

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def get_name(self):
        return self.username
class ClientVerificationCode(models.Model):
    code = models.CharField(max_length=4, blank=1, null=1)
    generate_time= models.DateTimeField(default=timezone.now)
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.code)
    @property
    def get_duration(self):
        return timezone.now() - self.generate_time
    @property
    def is_valid(self):
        #le code est valide si ça durrée est inferieur à 12h
        if(self.get_duration.days >= 1) : return False
        return self.get_duration.seconds < settings.CODE_EXPIRE_TIME

#signals 

@receiver(post_save, sender=ClientVerificationCode)
def create_verification_code(sender, instance, created, *args, **kwargs):
    if created:
        while True:
            code = randrange(1000, 10000)
            if not ClientVerificationCode.objects.filter(code=code).exists():
                instance.code = code
                instance.save()
                break
        send_mail("Email verification", "%s"%instance.code, "master@admin.tg", [instance.client.email,])

@receiver(post_save, sender=Client)
def create_client(sender, instance, created, *args, **kwargs):
    if created:
        VerificationCode = ClientVerificationCode.objects.create(client=instance)
        VerificationCode.save()
class ClientLoginCode(ClientVerificationCode):
    pass
"""


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
"""

