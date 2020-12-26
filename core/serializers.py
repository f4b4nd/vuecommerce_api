from rest_framework import serializers

from .models import Product, Order, Comment, ProductTopic, ProductGroups
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
        fields = ('title', 'description', 'resume', 'price', 'img', 'created_at', 'slug', 'comments')


class ProductGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGroups
        fields = ('id', 'name', 'slug')
        
class ProductTopicSerializer(serializers.ModelSerializer):
    groups = ProductGroupsSerializer(many=True)
    class Meta:
        model = ProductTopic
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

