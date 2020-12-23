
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
    Comment,
    ProductCategory,
    ProductSubCategory,
    )

from accounts.models import User
import random, string


## TOOLS ##

def get_random_instance(model, *args, **kwargs):

    if model == Address:
        choice = kwargs.get('choice', None)
        objs = model.objects.filter(address_type=choice)

    elif model == Payment:
        # OnetoOne relation between Order and Payment
        orders =  Order.objects.filter(payment__isnull=False)
        pks = [o.payment.pk for o in orders]
        objs = Payment.objects.exclude(pk__in=pks)

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

    if text == "uniq":
        # some text begins the same
        letters = string.ascii_lowercase
        res = ''.join(random.choice(letters) for i in range(max_length))
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


def generate_payments(request, times):
    for i in range(0, times):
        p = Payment()
        idx = random.randint(0, 1)
        p.method = ['S', 'P'][idx]
        p.charge_id = random_text('n', 15)
        p.amount = random.randint(1000, 9999) / 100
        p.save()
    return HttpResponse(f'{times} Payments generated !')


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


def generate_categories(request, times):
    for i in range(0, times):
        c = ProductCategory()
        c.name = random_text('uniq', 10)
        c.save()
    return HttpResponse(f'{times} Categories generated !')

def generate_subcategories(request, times):
    for i in range(0, times):
        c = ProductSubCategory()
        c.parent = get_random_instance(ProductCategory)
        c.name = random_text('uniq', 10)
        c.save()
    return HttpResponse(f'{times} SubCategories generated !')

# UPDATE

def update_orders(request):

    for p in Order.objects.all():
        
        if not p.bill_address:
            p.bill_address = get_random_instance(Address, choice='B')

        if not p.ship_address:
            p.ship_address = get_random_instance(Address, choice='S')

        if not p.payment:
            # NOTE: problem OneToOne
            p.payment = get_random_instance(Payment, relation='1to1')

        p.save()

    return HttpResponse('Order updated !')


def update_products(request, add_img=None):

    for p in Product.objects.all():
        
        if not p.category:
            p.category = get_random_instance(ProductCategory)

        if add_img == 'true':
            # Sets img 
            img_folder = f"{settings.BASE_DIR}/load-data/img"
            filenames = [files for _, _, files in os.walk(img_folder)][0]
            filename = filenames[random.randint(0, len(filenames)-1)]
            if not p.img:
                p.img.save(f'{filename}', File(open(f'{img_folder}/{filename}', 'rb')))

        p.save()

    return HttpResponse('Products updated !')

def update_templatesHTML(request):
    # for slug 
    for inf in TemplateHTML.objects.all():        
        inf.save()

    return HttpResponse('TemplateHTML updated !')

