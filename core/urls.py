from django.urls import path, include
from rest_framework import routers

from core import views


# HARDCODED VIEWS

urlpatterns = [
    path('api/informations/<slug:slug>', views.InformationView, name='Information'),

    # path('api/register-user/', views.RegisterUser, name='RegisterUser'),
    
]


# REST-FRAMEWORK

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='products')

urlpatterns += [path('api/',  include(router.urls))]


