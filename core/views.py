from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets

from .models import Product, Information
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@require_http_methods(["GET"])
def ProductView(request, slug):
    obj = get_object_or_404(Product, slug=slug)
    serialized_obj = ProductSerializer(obj)
    # status = 200
    return JsonResponse(serialized_obj.data)
    

@require_http_methods(["GET"])
def InformationView(request, slug):
    obj = get_object_or_404(Information, slug=slug)
    serialized_obj = serializers.serialize('json', [ obj, ], ensure_ascii=False)
    status = 200
    return JsonResponse(serialized_obj[1:-1], safe=False)


