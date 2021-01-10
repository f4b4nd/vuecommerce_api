from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .serializers import (
    OrderAddressSerializer,
    OrderSerializer,
)

from ecommerce.utils import get_objects_or_404, get_object_or_create


from .models import (
        Order,
        OrderProduct,
        Address,
        Payment,
    ) 

from products.models import Product


class OrderAddressAPI(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OrderAddressSerializer

    def post(self, request, *args, **kwargs):
        for address_type in ['ship_address', 'bill_address']:
            data = {**request.data}[address_type]
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
        return Response({})


    def get(self, request, *args, **kwargs):
        orders = get_objects_or_404(Order,
                                    user=request.user,
                                    ship_address__isnull=False,
                                    bill_address__isnull=False)

        order = orders.order_by('-created_at').first()

        ship = self.get_serializer(order.ship_address)
        bill = self.get_serializer(order.bill_address)
            
        return Response({
            'ship_address': ship.data,
            'bill_address': bill.data,
        })


class StripePaymentAPI(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = {**request.data}
        
        order = get_object_or_404(Order,
                                  user=self.request.user,
                                  payment__isnull=True)
            
        payment = Payment (
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
            raise Http404

        order, _ = get_object_or_create(Order,
                                        user=request.user,
                                        payment__isnull=True)
     
        # add products from frontend to order
        for p in cart:

            product = Product.objects.get(slug=p['slug'])
                    
            op, _ = get_object_or_create(OrderProduct,
                                         order=order,
                                         product=product)
            op.quantity = p['quantity']
            op.save()

        # remove products from backend that are not in frontend cart
        cart_pks = [c['id'] for c in cart]
        order.orderproducts.exclude(
            product__pk__in=cart_pks
            ).delete()

        # remove empty orders with no payment (when transaction succeeds)
        if len(cart) == 0:
            order = get_object_or_404(Order,
                                      user=request.user, 
                                      payment__isnull=True)
            order.delete()

        return Response({})


class OrderViewSet(viewsets.ModelViewSet):
    # TODO: post + tokenauth + permissions.isAuth
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
