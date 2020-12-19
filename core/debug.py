
from django.conf import settings
from django.http import HttpResponse
from django.core.files import File
import os, random, lorem
from core.models import Product, Information


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

def update_informations(request):
    # for slug 
    for inf in Information.objects.all():        
        inf.save()

    return HttpResponse('Informations updated !')