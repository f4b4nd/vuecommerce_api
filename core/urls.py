from django.urls import path, include
from rest_framework import routers

from .views import ProductViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')


urlpatterns = [
    path('api/',  include(router.urls))
]