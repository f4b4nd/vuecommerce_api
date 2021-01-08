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

class SaveAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('first_name', 'last_name', 'address', 'zipcode', 'country', 'city', 'address_type')


    def create(self, validated_data):
        # NOTE: the command should already exist, got to use a return

        try:
            order = Order.objects.get(
                user=self.context['request'].user,
                payment=None
            )
        except Order.DoesNotExist:
            return

        try:
            address = Address.objects.create(**validated_data)
        except IntegrityError:
            return

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

