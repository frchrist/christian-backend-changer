from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from Authentication import views
from django.conf import settings
auth_router = SimpleRouter()


#this is for debuging users model
# in production this in going to be disable
if settings.DEBUG:
    auth_router.register("list", views.ListClient, basename="list-user" )
auth_router.register("register", views.AddClient, basename="register-user")
urlpatterns  = [
    path("", include(auth_router.urls)),
    path("verified/", views.VerifiedClient.as_view(), name="verification-user"),
    path("list-users/<int:pk>/", views.ListSubUser.as_view(), name="listing"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
