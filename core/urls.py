from django.urls import path, include
from django.conf import settings
from rest_framework import routers

from core import views


# HARDCODED VIEWS

urlpatterns = [
    path('api/informations/<slug>', views.InformationView, name='Information'),
    path('api/product/<slug>', views.ProductView, name='ProductView'),
]


# REST-FRAMEWORK

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='products')

urlpatterns += [path('api/',  include(router.urls))]


# DEBUG

if settings.DEBUG:
    urlpatterns += [path('product_update', views.auto_product_update, name='save_slugs')]
