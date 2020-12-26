from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from django.db import IntegrityError

from .models import Product, TemplateHTML, Order, Comment, ProductTopic
from .serializers import ProductSerializer, OrderSerializer, CommentSerializer, ProductTopicSerializer
import random, string

from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

class ProductTopicViewSet(viewsets.ModelViewSet):
    queryset = ProductTopic.objects.all()
    serializer_class = ProductTopicSerializer

class OrderViewSet(viewsets.ModelViewSet):
    # TODO: post + tokenauth + permissions.isAuth
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


@require_http_methods(["GET"])
def ProductView(request, slug):
    obj = get_object_or_404(Product, slug=slug)
    serialized_obj = ProductSerializer(obj)
    # status = 200
    return JsonResponse(serialized_obj.data)
    

@require_http_methods(["GET"])
def InformationView(request, slug):
    obj = get_object_or_404(TemplateHTML, slug=slug)
    serialized_obj = serializers.serialize('json', [ obj, ], ensure_ascii=False)
    status = 200
    return JsonResponse(serialized_obj[1:-1], safe=False)


