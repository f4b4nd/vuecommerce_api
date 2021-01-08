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
class CheckoutAddressAPI(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = core_serializers.SaveAddressSerializer

    def post(self, request, *args, **kwargs):
        
        for address_type in ['ship_address', 'bill_address']:
            data = {**request.data}[address_type]
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
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
        
        if request.user:

            order, _ = Order.objects.get_or_create(
                    user=request.user, 
                    payment=None
                )

             # data parse
            cart = request.data

            # add products from frontend to order
            for data in cart:
                product = Product.objects.get(slug=data['slug'])
                        
                op, _ = OrderProduct.objects.get_or_create(
                    order=order,
                    product=product,
                )
                op.quantity = data['quantity']
                print(data, _)
                op.save()

            # remove products from backend that are not in frontend cart
            cart_products = [c['id'] for c in cart]
            order.orderproducts.exclude(
                    product__pk__in=cart_products
                ).delete()

        return Response({})

class OrderViewSet(viewsets.ModelViewSet):
    # TODO: post + tokenauth + permissions.isAuth
    queryset = Order.objects.all()
    serializer_class = core_serializers.OrderSerializer

