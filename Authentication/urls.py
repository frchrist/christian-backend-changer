from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from Authentication import views
from django.conf import settings

urlpatterns  = [
    path("email/verification/", views.VerifiedClient.as_view(), name="verification_client_email"),
    path("refresh/email/verification/code", views.ClientNewCode.as_view(), name="refresh_client_vf_code"),
    path("signin/",views.LoginAPIView.as_view(), name="login"),
    path("signup/",views.RegisterAPIView.as_view(), name="register"),
    path("signout/", views.Logout.as_view(), name="logout"),
    path("signin/twofactor/client_id=none",views.TwoFactorAuth.as_view(), name="two_factor_auth"),
    #reset user password preccess
    path("change/password/", views.RequestChangePasswordView.as_view(), name="request_email"),
    path("change/password/check/data/<uidb64>/<token>/",views.PasswordTokenCheckAPI.as_view(), name="request_comfirm"),
    path("change/password/complete/",views.SetNewPasswordAPIView.as_view(), name="request_complete" ),
    # refresh user access token
    path('token/refresh/', views.CookieTokenRefreshView.as_view(), name='token_refresh'),

]
