from django.utils.translation import gettext_lazy as _
from rest_framework import (mixins, viewsets)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from .serializers import TwoFactorAuthSerializer
from .serializers import (WriteClientSerializer,ReadClientSerializer, LoginSerializer,
         RequestChangePasswordSerializer, RequestPostNewPasswordSerializer,
          CodeSerializer, CookieTokenRefreshSerializer)
from .models import Client , ClientVerificationCode, ClientLoginCode

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenRefreshView

from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,  urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .mail import AsynEmailMessage
from django.urls import reverse
from django.conf import settings
from rest_framework.throttling import UserRateThrottle
from jwt import decode
"""
author : christi@n
date  :  06/08/2021
API for crypto currency exchange
"""


class ClientNewCode(GenericAPIView):
    serializer_class = RequestChangePasswordSerializer
    """
    this view is for if user is login and want to activate there account
    """
    def post(self,request):
        email = request.data['email']
        code = None
        try:
            code = ClientVerificationCode.objects.get(client__email=email)
        except:
            pass
        if code != None:code.delete()
        if Client.objects.filter(email=email).exists():
            create_code(Client.objects.get(email=email))
        return Response({"detail":_("a code has been send to your email address")}, status=201)
    
class Logout(GenericAPIView):
    def post(self, request):
        response = Response()
        response.set_cookie("__refresh_token", "", max_age=0, httponly=True)
        response.data = {}
        return response


class TwoFactorAuth(GenericAPIView):
    serializer_class = TwoFactorAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = Response()
        data = serializer.data
        if data["refresh"]:
            cookie_max_age =settings.COOKIE_AGES
            response.set_cookie('__refresh_token', data["refresh"], max_age=cookie_max_age, httponly=True )
            del data["refresh"]
        response.data = data
        return response


class VerifiedClient(GenericAPIView):
    serializer_class  = CodeSerializer
    # throttle_classes = [UserRateThrottle]
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"detail": _("your account has been successfully activate")},status=200)

class RegisterAPIView(GenericAPIView):
    serializer_class = WriteClientSerializer
    querset = Client.objects.all()
    def post(self,request):
        serializer = self.serializer_class(data=request.data) 
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

class CookieTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("access",None):
            user_payload = decode(response.data["access"], settings.SECRET_KEY,  algorithms="HS256")
            user = Client.objects.get(id=int(user_payload["user_id"]))
            response.data["username"]  = user.username
            response.data["email"]  = user.email
        if response.data.get('refresh'):
            cookie_max_age = settings.COOKIE_AGES
            response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True )
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)
    serializer_class = CookieTokenRefreshSerializer

class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data) 
        serializer.is_valid(raise_exception=True)
        response = Response()
        data = serializer.data
        
        if data["refresh"]:
            cookie_max_age = 3600 * 24 * 14 # 14 days
            response.set_cookie('__refresh_token', data["refresh"], max_age=cookie_max_age, httponly=True )
            del data["refresh"]
        response.data = data
        return response

class RequestChangePasswordView(GenericAPIView):
    serializer_class = RequestChangePasswordSerializer
    def post(self, request):
        email = request.data['email']
        user = None
        try:
            user = Client.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            # domain = get_current_site(request).domain
            # relatedLink = reverse("password-reset-confirm", kwargs={"uidb64":uidb64, "token":token})
            # absurl = "http://"+domain+relatedLink
            redirect_front_end_url ="http://"+ settings.FRONTEND_URL+"/auth/accounts/reset-password/"+uidb64+"/"+token
            email_body = "Hello \n use this link to reset your password  \n"+redirect_front_end_url
            data = {
                "email_body":email_body,
                "email_subject":'reset your password',
                "email_to":(user.email,),
            }
            email_instance = AsynEmailMessage(data)
            email_instance.start()
        except Exception as e:
            pass
            
        return Response({"detail":_("He have set you the link to reset your password")}, status=status.HTTP_200_OK)

class PasswordTokenCheckAPI(APIView):
    def get(self, request, uidb64 , token):
        try:
           id = smart_str(urlsafe_base64_decode(uidb64))
           user = Client.objects.get(id=id)
           if not PasswordResetTokenGenerator().check_token(user, token):
               return Response({"detail":_("Token is not valid, please request a new one")}, status=status.HTTP_400_BAD_REQUEST)
           return Response({"detail":True, "message":"Credentials Valid", "uibd64":uidb64, "token":token}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError:
            return Response({"detail":_("Token is not valid, please request a new one")}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail":_("Token is not valid, please request a new one")}, status=status.HTTP_400_BAD_REQUEST)



class SetNewPasswordAPIView(GenericAPIView):
    serializer_class = RequestPostNewPasswordSerializer
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"detail":True}, status=status.HTTP_200_OK)
