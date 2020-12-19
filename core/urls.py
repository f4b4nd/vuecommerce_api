from django.urls import path, include
from django.conf import settings
from rest_framework import routers

from core import views


# HARDCODED VIEWS

urlpatterns = [
    path('api/informations/<slug:slug>', views.InformationView, name='Information'),
    path('api/product/<slug:slug>', views.ProductView, name='ProductView'),
]


# REST-FRAMEWORK

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='products')

urlpatterns += [path('api/',  include(router.urls))]


# DEBUG

if settings.DEBUG:

    from core import debug

    urlpatterns += [
        path('generate_products/<int:times>', debug.generate_products, name='generate_products'),
        path('update_products', debug.update_products, name='update_products'),
        path('update_informations', debug.update_informations, name='update_informations'),
    ]
