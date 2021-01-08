from django.conf import settings

from rest_framework import viewsets
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .serializers import (
    CheckoutAddressSerializer,
    OrderSerializer,
)

from .models import (
        Order,
        OrderProduct,
        Address,
        Payment,
    ) 

from products.models import Product


class CheckoutAddressAPI(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CheckoutAddressSerializer

    def post(self, request, *args, **kwargs):
        for address_type in ['ship_address', 'bill_address']:
            data = {**request.data}[address_type]
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()

        return Response({})

    def get(self, request, *args, **kwargs):
        order = Order.objects.filter(
            user=request.user,
            ship_address__isnull=False,
            bill_address__isnull=False,
        ).order_by('-created_at').first()
        
        if order:
            ship = CheckoutAddressSerializer(order.ship_address)
            bill = CheckoutAddressSerializer(order.bill_address)
            
            return Response({
                'ship_address': ship.data,
                'bill_address': bill.data,
            })


class StripePaymentAPI(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = {**request.data}

        try:
            order = Order.objects.get(
                user=self.request.user,
                payment__isnull=True,
            )
        except Order.DoesNotExist:
            return Response({})

        payment = Payment.objects.create(
            charge_id = data['transactionToken'],
            service = data['service'],
            amount = data['amount']
        )
        
        order.payment = payment
        order.save()

        return Response({})


class UpdateCartAPI(generics.GenericAPIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        # data parse
        cart = request.data

        if not request.user:
            return Response({})

        order, created = Order.objects.get_or_create(
                user=request.user, 
                payment__isnull=True,
            )
        
        # add products from frontend to order
        for data in cart:
            product = Product.objects.get(slug=data['slug'])
                    
            op, _ = OrderProduct.objects.get_or_create(
                order=order,
                product=product,
            )
            op.quantity = data['quantity']
            op.save()

        # remove products from backend that are not in frontend cart
        cart_products = [c['id'] for c in cart]
        order.orderproducts.exclude(
                product__pk__in=cart_products
            ).delete()

        # remove empty orders with no payment (when transaction succeeds)
        if len(cart) == 0:
            try:
                order = Order.objects.get(user=request.user, 
                                          payment__isnull=True)                                        
                order.delete()
            except Order.DoesNotExist:
                pass
                    
        return Response({})


class OrderViewSet(viewsets.ModelViewSet):
    # TODO: post + tokenauth + permissions.isAuth
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

