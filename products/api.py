from django.conf import settings

from rest_framework import viewsets
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .serializers import (
        ProductSerializer,
        ProductTopicSerializer,
)

from .models import (
        Product,
        ProductTopic,
    ) 

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'


class ProductTopicViewSet(viewsets.ModelViewSet):
    queryset = ProductTopic.objects.all()
    serializer_class = ProductTopicSerializer