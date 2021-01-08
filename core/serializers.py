from django.db import IntegrityError
from rest_framework import serializers

from .models import Product, Order, Comment, ProductTopic, ProductGroups, Address
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email") 

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'resume', 'price', 'img', 'created_at', 'slug', 'comments')


class ProductGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGroups
        fields = ('id', 'name', 'slug')
        
class ProductTopicSerializer(serializers.ModelSerializer):
    groups = ProductGroupsSerializer(many=True)
    class Meta:
        model = ProductTopic
        fields = ('id', 'name', 'slug', 'groups')

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

