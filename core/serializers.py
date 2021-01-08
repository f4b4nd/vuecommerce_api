from django.db import IntegrityError
from rest_framework import serializers

from .models import (
    Order,  Address,
)

# from products.models import (Product, ProductTopic, ProductGroups, Comment,)


class CheckoutAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('first_name', 'last_name', 'address', 'zipcode', 'country', 'city', 'address_type')
        validators = [] # unique_together not checked because it blocks serializer.is_valid()

    def create(self, validated_data):

        try:
            order = Order.objects.get(
                user=self.context['request'].user,
                payment__isnull=True
            )
        except Order.DoesNotExist:
            return
        
        address, _ = Address.objects.get_or_create(**validated_data)
        
        if validated_data['address_type'] == 'S':
            order.ship_address = address

        elif validated_data['address_type'] == 'B':
                order.bill_address = address
    
        order.save()
        return order

    # def perform_create(self, serializer):
    #     serializer.save()



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

