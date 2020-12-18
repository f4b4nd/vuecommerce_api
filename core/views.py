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



if settings.DEBUG: 

    from django.core.files import File
    import os, random, lorem


    def generate_products(request, times):
        for i in range(0, times):
            p = Product(
                title=lorem.sentence()[:-1],
                resume=lorem.paragraph(),
                description=lorem.text(),
                price=round(100 * random.random(), 2)
            )
            p.save()
        return HttpResponse(f'{times} Products created !')

    def update_products(request):

        for p in Product.objects.all():
            
            # Sets img 
            img_folder = f"{settings.BASE_DIR}/load-data/img"
            filenames = [files for _, _, files in os.walk(img_folder)][0]
            filename = filenames[random.randint(0, len(filenames)-1)]
            if not p.img:
                p.img.save(f'{filename}', File(open(f'{img_folder}/{filename}', 'rb')))

            # Save for slug
            p.save()

        return HttpResponse('Products updated !')