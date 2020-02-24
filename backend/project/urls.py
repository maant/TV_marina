from django.conf.urls import url
from django.urls import include, path

from rest_framework import routers

from bankapi.views import UserViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include('bankapi.urls'))
]
