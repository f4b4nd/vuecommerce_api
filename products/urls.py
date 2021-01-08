from django.urls import path, include
from rest_framework import routers

from products import api

# HARDCODED VIEWS

urlpatterns = [
        
]


# REST-FRAMEWORK

router = routers.DefaultRouter()
router.register(r'products', api.ProductViewSet, basename='products')
router.register(r'topics', api.ProductTopicViewSet, basename='topics')


urlpatterns += [path('api/',  include(router.urls))]
