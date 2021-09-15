from django.apps import apps
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from .validators import PhoneNumberValidator, UsernameValidator
from .mail import AsynEmailMessage
from random import randrange
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

class Client(AbstractBaseUser, PermissionsMixin):
    username_validator = UsernameValidator()

    phone_number_validator = PhoneNumberValidator()
    username = models.CharField(
        _('Nom Utilisateur'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with tihat username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=False,
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        })
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    email_is_valid = models.BooleanField(
        _("valid_email"),
        default=False,
        help_text=_(
            'Designates whether the client email is valid or not'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    sponsor = models.ForeignKey(to="self", on_delete=models.CASCADE, blank=True, null=True)

    balance = models.PositiveIntegerField(
        _("balance"),
        default=0,
        help_text=_("Designed the balance of the client")
    )

    notification = models.BooleanField(
        _('notification'),
        default=False,
        help_text=_(
            'Designed whether this client can recieve notifications'
        ),
    )

    double_auth = models.BooleanField(
        _('double authentication'),
        default=False,
        help_text=_(
            'Designed whether if client has double authentication or not'
        ),
    )

    phone_number = models.CharField(
        _("phone_number"),
        max_length=20,
        default=None,
        blank=True,
        null=True,
        validators=[phone_number_validator],
        help_text=_(
            "Designed the phone number of the client or user"
        )
    )
    city = models.CharField(
        _("city"),
        max_length=20,
        default="Togo",
        blank=False,
        help_text = _(
            "Designant whether the client city is"
        )
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True


    def has_module_perms(self, app_label):
        return True

    def token(self):
        tokens = RefreshToken.for_user(self)

        return {
            "refresh":str(tokens),
            "access":str(tokens.access_token)
        }

    @property
    def access_token(self):
        return self.token()["access"]

    @property
    def refresh_token(self):
        return self.token()["refresh"]
    
    @property
    def get_token(self):
        pass
    @property
    def get_balance(self):
        return self.balance
    @property
    def is_valid(self):
        return self.email_is_valid

    @property
    def can_be_notify(self):
        return self.notification


    @property
    def get_name(self):
        return self.username

class ClientVerificationCode(models.Model):
    code = models.CharField(
        max_length=8,
        blank=1,help_text=_("Designed this code or register client")
    )
    create_at = models.DateTimeField(default=timezone.now)
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE,
        help_text=_("Designant whether client instance")
        )

    def __str__(self):
        return  self.client.username
    @property
    def get_duration(self):
        return timezone.now() - self.create_at
    @property
    def is_valid(self):
        #le code est valide si ça durrée est inferieur à 12h
        if(self.get_duration.days >= 1) : return False
        return self.get_duration.seconds < settings.CODE_EXPIRE_TIME

class ClientLoginCode(ClientVerificationCode):
    pass


#signals 

@receiver(post_save, sender=ClientVerificationCode)
@receiver(post_save, sender=ClientLoginCode)
def create_verification_code(sender, instance, created, *args, **kwargs):
    if created:
        while True:
            code = randrange(10000, 100000)
            if not sender.objects.filter(code=code).exists():
                instance.code = code
                instance.save()
                break
        data = {
            "email_subject":_("Verification Email"),
            "email_body":str(instance.code),
            "email_from":settings.EMAIL_HOST,
            "email_to":[instance.client.email,]
        }

        email_instance = AsynEmailMessage(data)
        email_instance.start()
@receiver(post_save, sender=Client)
def create_client(sender, instance, created, *args, **kwargs):
    if created:
        VerificationCode = ClientVerificationCode.objects.create(client=instance)
        VerificationCode.save()
