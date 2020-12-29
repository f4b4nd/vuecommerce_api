from django.conf import settings

from rest_framework import viewsets
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from . import models as core_models 
from . import serializers as core_serializers


class ProductViewSet(viewsets.ModelViewSet):
    queryset = core_models.Product.objects.all()
    serializer_class = core_serializers.ProductSerializer
    lookup_field = 'slug'

class ProductTopicViewSet(viewsets.ModelViewSet):
    queryset = core_models.ProductTopic.objects.all()
    serializer_class = core_serializers.ProductTopicSerializer

# Register API
class SaveAddressAPI(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = core_serializers.SaveAddressSerializer

    def post(self, request, *args, **kwargs):
        data = {**request.data}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)    
        order = serializer.save()
        return Response({
            "status": "ok",
        })


class OrderViewSet(viewsets.ModelViewSet):
    # TODO: post + tokenauth + permissions.isAuth
    queryset = core_models.Order.objects.all()
    serializer_class = core_serializers.OrderSerializer

    



