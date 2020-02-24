from django.conf.urls import url
from django.urls import include, path

from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'accounts', views.BankAccountViewSet)
router.register(r'transactions', views.BankTransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
