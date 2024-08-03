# use default router with urlpattern
from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import ObtainAuthToken

router = DefaultRouter()


urlpatterns = [
    path('api-token-auth/', ObtainAuthToken.as_view(), name='api_token_auth'),
] + router.urls