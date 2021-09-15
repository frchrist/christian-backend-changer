
from django.urls import include, path
from .views import TransactionViews, WithdrawViews
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'change', TransactionViews)
router.register(r'withdraw', WithdrawViews)

urlpatterns = [
        path('', include(router.urls)),
]






