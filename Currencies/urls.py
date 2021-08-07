from django.urls import path, include
from rest_framework.routers import SimpleRouter
from Currencies import views
router = SimpleRouter()
router.register("list",views.ListCurrencies, basename="list-currencies" )
urlpatterns = [

     path("", include(router.urls))
 ]
