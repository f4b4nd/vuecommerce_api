from django.db import IntegrityError
from rest_framework import serializers

from .models import (
    Order,  Address,
)

from django.shortcuts import get_object_or_404
from ecommerce.utils import get_object_or_create


class OrderAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('first_name', 'last_name', 'address', 'zipcode', 'country', 'city', 'address_type')
        validators = [] # unique_together not checked because it blocks serializer.is_valid()

    def create(self, validated_data):
        
        order = get_object_or_404(Order,
                                  user=self.context['request'].user,
                                  payment__isnull=True)
        
        address, _ = get_object_or_create(Address, **validated_data)
        
        if validated_data['address_type'] == 'S':
            order.ship_address = address

        elif validated_data['address_type'] == 'B':
                order.bill_address = address
    
        order.save()
        return order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

