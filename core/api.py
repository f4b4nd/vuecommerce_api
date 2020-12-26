from django.conf import settings

from rest_framework import viewsets
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication

from . import models as core_models 
from . import serializers as core_serializers


class ProductViewSet(viewsets.ModelViewSet):
    queryset = core_models.Product.objects.all()
    serializer_class = core_serializers.ProductSerializer
    lookup_field = 'slug'

class ProductTopicViewSet(viewsets.ModelViewSet):
    queryset = core_models.ProductTopic.objects.all()
    serializer_class = core_serializers.ProductTopicSerializer

class OrderViewSet(viewsets.ModelViewSet):
    # TODO: post + tokenauth + permissions.isAuth
    queryset = core_models.Order.objects.all()
    serializer_class = core_serializers.OrderSerializer

    



