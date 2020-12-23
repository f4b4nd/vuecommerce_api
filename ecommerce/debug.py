
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


## TOOLS ##

def get_random_instance(model, *args, **kwargs):

    if model == Address:
        choice = kwargs.get('choice', None)
        objs = model.objects.filter(address_type=choice)
    else:
        objs = model.objects.all()
    
    if objs.count() == 0:
        return
    index = random.randint(0, objs.count()-1)
    keys = [m.pk for m in objs]

    return objs.filter(pk=keys[index]).first()


def random_text(text, max_length=None):
    res = ""
    if text == "t":
        res = lorem.text()
        res = re.sub("\.", "", res)
    elif text == 'n' and max_length:
        res = str([random.randint(1, 9) for i in range(0, max_length)])
        res = re.sub("\[|\]|\,|\s", "", res)
    if max_length:
        return res[:max_length]
    return res


## GENERATE ##

def generate_products(request, times):
    for i in range(0, times):
        p = Product()
        p.title = random_text('t', 80)
        p.resume = random_text('t', 500)
        p.description = random_text('t')
        p.price = round(100 * random.random(), 2)
        p.save()
    return HttpResponse(f'{times} Products created !')

def generate_orders(request, times):
    for i in range(0, times):
        o = Order()
        o.user = get_random_instance(User)
        o.bill_address =  get_random_instance(Address, choice='B')
        o.ship_address = get_random_instance(Address, choice='S')
        o.payment = get_random_instance(Payment)
        o.save()
    return HttpResponse(f'{times} Orders generated !')


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



# UPDATE
def update_products_img(request):

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



#


#
def add_orderproducts_to_orders(request, times):
    pass

#
def generate_comments(request):
    pass    
