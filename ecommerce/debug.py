
from django.conf import settings
from django.http import HttpResponse
from django.core.files import File
import os, random, lorem, re
from core.models import (
    Product, 
    TemplateHTML, 
    Order,
    Address,
    Payment,
    )

from accounts.models import User
import random

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

def update_templatesHTML(request):
    # for slug 
    for inf in TemplateHTML.objects.all():        
        inf.save()

    return HttpResponse('TemplateHTML updated !')

def get_random_instance(model):
    objs = model.objects.all()
    if objs.count() == 0:
        return
    index = random.randint(0, objs.count())
    keys = [m.pk for m in objs] 
    return objs.filter(pk=keys[index]).first()

def random_text(text, max_length):
    res = ""
    if text == "t":
        res = lorem.text()
        res = re.sub("\.", "", res)
    elif text == 'n':
        res = str([random.randint(1, 9) for i in range(0, max_length-1)])
        res = re.sub("\[|\]|\,|\s", "", res)
    return res[:max_length]

#
def generate_orders(request, times):
    for i in range(0, times):
        o = Order()
        o.user = get_random_instance(User)
        o.bill_address =  get_random_instance(Address)
        o.ship_address = get_random_instance(Address)
        o.payment = get_random_instance(Payment)
        o.save()
    return HttpResponse(f'{times} Orders generated !')

#
def generate_addresses(request, times):
    for i in range(0, times):
        a = Address()

        idx = random.randint(0, 1)
        a.address_type = ['B', 'S'][idx]
        a.first_name = random_text('t', 15)
        a.last_name = random_text('t', 15)
        a.address = random_text('t', 50)
        a.zipcode = random_text('n', 5)
        a.country = random_text('t', 10)
        a.city = random_text('t', 10)
        a.save()
    return HttpResponse(f'{times} Addresses generated !')

#
def add_orderproducts_to_orders(request, times):
    pass

#
def generate_comments(request):
    pass    
