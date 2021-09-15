from Authentication.utils import Utils
from .models import Client,ClientVerificationCode, ClientLoginCode
from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,  urlsafe_base64_encode
from django.contrib.auth import password_validation
from django.core import exceptions as dj_except

from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken

class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None
    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('__refresh_token')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken('No valid token found in cookie \'refresh_token\'')


class ReadClientSerializer(serializers.ModelSerializer):
    sponsor = serializers.SlugRelatedField(slug_field="username", queryset=Client.objects.all())
    class Meta:
        model = Client
        fields = ["id", "username","email", "balance", "phone_number", "last_name", "first_name", "sponsor", "email_is_valid", "notification"]
        read_only_fields = fields



class WriteClientSerializer(serializers.ModelSerializer):
    sponsor = serializers.SlugRelatedField(slug_field="username",allow_null=True, queryset=Client.objects.all())
    class Meta:
        model = Client
        fields = ["username",'email',"phone_number","password","sponsor"]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.get("password", None)
        model = self.Meta.model(**validated_data)
        if password is not None:
            model.set_password(password)
        model.save()

        return model


    def validate(self, data):
        client = Client(**data)
        password = data.get("password", None)
        errors = dict()
        try:
            password_validation.validate_password(password=password, user=Client)
        except dj_except.ValidationError as e:
            errors['password'] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        return super().validate(data)


class CodeSerializerAbstract(serializers.Serializer):
    code = serializers.CharField(max_length=255, write_only=True)


class CodeSerializer(CodeSerializerAbstract):
    email = serializers.EmailField(max_length=255, min_length=4)

    def validate(self, attrs):
        code = attrs.get("code", None)
        email = attrs.get("email", None)

        try:
            current_code = Utils.authenticate_with_vf_code(code=code, email=email)
            client = current_code.client
            if current_code.is_valid:
                client = current_code.client
                if not client.email_is_valid:
                    client.email_is_valid = True
                    client.save()
                current_code.delete()
                return {"email":email}
            else:
                Utils.create_email_verification_code(client)
                raise TypeError
        except Exception as e:
            print(e)
            cli = Utils.client_from_mail(email)
            if cli:
                Utils.create_email_verification_code(cli)
            raise ValidationError({"errors":_("please check your mails and try again")})



class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=4)
    password = serializers.CharField(max_length=68, write_only=True)
    username = serializers.CharField(max_length=255, read_only=True)
    refresh = serializers.CharField(max_length=255, read_only=True)
    access = serializers.CharField(max_length=255, read_only=True)

    redirect = serializers.BooleanField( read_only=True)
    class Meta:
        model = Client
        fields = ("email", "password", "username", "refresh","access" ,"redirect")


    def validate(self,attrs):
        email =attrs.get("email", None)
        password = attrs.get("password", None)

        user_instance = auth.authenticate(email=email, password=password)
        if user_instance:
            if not user_instance.email_is_valid:
                raise AuthenticationFailed(_("Email address is not verified"))
            if user_instance.double_auth:
                Utils.create_login_code(user_instance)
                return {
                    "email":"",
                    "username":"",
                    "refresh":"",
                    'access':"",
                    "redirect":True
                }
            return {
                    "email":user_instance.email,
                    "username":user_instance.username,
                    "refresh":user_instance.refresh_token,
                    "access":user_instance.access_token,
                    "redirect":False
                }
        raise AuthenticationFailed(_("Invalid credentials"))


class TwoFactorAuthSerializer(LoginSerializer, CodeSerializerAbstract):
    class Meta:
        model = Client
        fields = ("email","username", "refresh", "access", "code" , "password")
    def validate(self, attrs):
        code = attrs.get("code", None)
        email = attrs.get("email", None)
        password = attrs.get("password", None)
        user_instance = auth.authenticate(email=email,password=password)
        code_instance = None
        try:
            code_instance = ClientLoginCode.objects.get(client=user_instance, code=code)
            if code_instance.is_valid:
                code_instance.delete()
                return {
                        "email":user_instance.email,
                        "username":user_instance.username,
                        "access":user_instance.access_token,
                        "refresh":user_instance.refresh_token,

                    }
            raise TypeError
        except Exception as e:
            if user_instance:
               Utils.create_login_code(user_instance)
            raise AuthenticationFailed(_("Authentication code is invalid"))
  
class RequestChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    class Meta:
        fields = ["email"]

class RequestPostNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=255, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ["password",'token','uidb64' ]

    def validate(self,attrs):
        try:
            password = attrs.get("password", "")
            token = attrs.get("token", "")
            uidb64 = attrs.get("uidb64", "")
            id = force_str(urlsafe_base64_decode(uidb64))
            user = Client.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("Link is invalid")
            user.set_password(password)
            
            user.save()
        except:
            raise AuthenticationFailed("Link is invalid")
        return super().validate(attrs)
