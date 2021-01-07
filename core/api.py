from django.conf import settings

from rest_framework import viewsets
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from . import serializers as core_serializers
from .models import (
        Order,
        OrderProduct,
        Product,
        ProductTopic,
    ) 


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = core_serializers.ProductSerializer
    lookup_field = 'slug'

class ProductTopicViewSet(viewsets.ModelViewSet):
    queryset = ProductTopic.objects.all()
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


class StripePaymentAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        data = {**request.data}
        print(data)
        return Response({
            "status": "ok",
        })

class UpdateCartAPI(generics.GenericAPIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        # data parse
        data = request.data[0]

        if request.user:

            order, _ = Order.objects.get_or_create(
                    user=request.user, 
                    payment=None
                )

            product = Product.objects.get(slug=data['slug'])
                    
            op, _ = OrderProduct.objects.get_or_create(
                order=order,
                product=product,
            )
            op.quantity = data['quantity']
            op.save()

        return Response({})

class OrderViewSet(viewsets.ModelViewSet):
    # TODO: post + tokenauth + permissions.isAuth
    queryset = Order.objects.all()
    serializer_class = core_serializers.OrderSerializer

