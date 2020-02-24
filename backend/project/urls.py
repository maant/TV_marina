from django.contrib.auth import views as auth_views
from django.urls import include, path

from rest_framework import routers

from backend.bankapi import views as bankapi_views
from . import views


router = routers.DefaultRouter()
router.register(r'users', bankapi_views.UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
# login
    path('login/', views.login_request, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
