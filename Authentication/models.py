from django.db import models


# Create your models here.
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, username,phone_number, first_name=None, last_name=None, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone_number, first_name=None, last_name=None, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
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
        max_length=255,
        unique=True,
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
    sponsor_id = models.IntegerField(null=1, blank=1)

    is_active = models.BooleanField(default=True)

    is_admin = models.BooleanField(default=False)
    balance = models.PositiveIntegerField(default=0)
    is_verifed = models.BooleanField(default=False)
    can_receive_notification = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'phone_number']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True


    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def get_balance(self):
        return self.balance
    @property
    def is_verifed(self):
        return self.is_verifed

    @property
    def can_notify(self):
        return self.can_receive_notification

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class ClientVerificationCode(models.Model):
    code = models.CharField(max_length=4)
    generate_time= models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.code
