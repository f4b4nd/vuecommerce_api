from django.db import IntegrityError
from rest_framework import serializers

from .models import (
    Product, ProductTopic, ProductGroups, Comment,
)

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

class ProductGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGroups
        fields = ('id', 'name', 'slug')


class ProductSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    groups = ProductGroupsSerializer(many=True)
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'resume', 'price', 'img', 'created_at', 'slug', 'comments', 'groups')

        
class ProductTopicSerializer(serializers.ModelSerializer):
    groups = ProductGroupsSerializer(many=True)
    class Meta:
        model = ProductTopic
        fields = ('id', 'name', 'slug', 'groups')