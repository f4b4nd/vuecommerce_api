
from django.conf import settings
from django.http import HttpResponse
from django.core.files import File
import os, random, lorem, re, string

from . import get_random_instance, random_text

from products.models import (
    Product, 
    Comment,
    ProductGroups,
    ProductTopic,
    ProductCoupon,
)

from accounts.models import User


## GENERATE ##


# PRODUCTS

def generate_products(request, times):
    for i in range(0, times):
        p = Product()
        p.title = random_text('t', 80)
        p.resume = random_text('t', 500)
        p.description = random_text('t')
        p.price = round(100 * random.random(), 2)
        #p.category = get_random_instance(ProductCategory)
        p.save()
    return HttpResponse(f'{times} Products created !')


def generate_comments(request, times):
    for i in range(0, times):
        c = Comment()
        c.post = get_random_instance(Product)
        c.user = get_random_instance(User)
        c.body = random_text('t', 200)
        c.rating = random.randint(1, 5)
        c.active = [True, False][random.randint(0, 1)]
        c.save()
    return HttpResponse(f'{times} Comments generated !')


def generate_productgroups(request, times):
    for i in range(0, times):
        g = ProductGroups()
        g.name = random_text('uniq', 10)
        g.topic = get_random_instance(ProductTopic)
        g.save()
    return HttpResponse(f'{times} ProductGroups generated !')



def update_topics(request):
    
    for t in ProductTopic.objects.all():
        t.delete()
    
    topics = ('high-tech', 'cuisine', 'maison', 'beauté', 'livres',)
    for topic in topics:
        t = ProductTopic()
        t.name = topic
        t.save()

    return HttpResponse(f'Topics updated !')

def add_groups_to_products(request):
    for p in Product.objects.all():
        # manytomany
        g1 = get_random_instance(ProductGroups)
        g2 = get_random_instance(ProductGroups)
        
        g1.products.add(p)

        if g1.pk != g2.pk:
            g2.products.add(p)
    
    return HttpResponse(f'ProductGroups updated !')


def update_products(request, add_img=None):

    for p in Product.objects.all():

        if add_img == 'true':
            # Sets img 
            img_folder = f"{settings.BASE_DIR}/load-data/img"
            filenames = [files for _, _, files in os.walk(img_folder)][0]
            filename = filenames[random.randint(0, len(filenames)-1)]
            if not p.img:
                p.img.save(f'{filename}', File(open(f'{img_folder}/{filename}', 'rb')))

        p.save()

    return HttpResponse('Products updated !')





def generate_productcoupon(request, times):
    for i in range(0, times):

        c = ProductCoupon()

        if random.randint(0, 4) == 0:
            # set product for 1/5 products                 
            c.product = get_random_instance(Product)

        c.code = random_text('t', 6).replace(' ', '').upper()

        if random.randint(0, 1) == 0:
            c.amount = random.randint(5, 8)
        else:
            c.percent = round(0.1 * random.randint(101, 250), 2)

        c.save()
    return HttpResponse(f'{times} ProductCoupons generated !')


# UPDATE





