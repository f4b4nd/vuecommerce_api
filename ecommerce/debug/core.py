
from django.conf import settings
from django.http import HttpResponse
from django.core.files import File
import os, random, lorem, re, string

from . import get_random_instance, random_text


from core.models import (
    Order,
    OrderProduct,
    Address,
    Payment,
    Refund,
    TemplateHTML,
    )

from accounts.models import User 
from products.models import Product 




def generate_orders(request, times):
    for i in range(0, times):
        o = Order()
        o.user = get_random_instance(User)
        o.bill_address = get_random_instance(Address, choice='B')
        o.ship_address = get_random_instance(Address, choice='S')
        o.payment = get_random_instance(Payment, relation='Order')
        o.save()
    return HttpResponse(f'{times} Orders generated !')



def generate_orderproducts(request, times):
    for i in range(0, times):
        o = OrderProduct()
        o.order = get_random_instance(Order)
        o.product =  get_random_instance(Product)
        o.quantity = random.randint(1, 4)
        o.save()
    return HttpResponse(f'{times} OrderProducts generated !')


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
        p.service = ['S', 'P'][idx]
        p.charge_id = random_text('n', 15)
        p.amount = random.randint(1000, 9999) / 100
        p.save()
    return HttpResponse(f'{times} Payments generated !')



def generate_refunds(request, times):
    for i in range(0, times):
        r = Refund()
        r.order = get_random_instance(Order, relation='Refund')
        r.reason = random_text('t', 200)
        r.accepted = True if random.randint(0, 1) else False
        r.save()
    return HttpResponse(f'{times} Refunds generated !')



def update_orders(request):

    for p in Order.objects.all():
        
        if not p.bill_address:
            p.bill_address = get_random_instance(Address, choice='B')

        if not p.ship_address:
            # Ship and Bill are the same 1/2 times
            p.ship_address = get_random_instance(Address, choice='S')

        if not p.payment:
            # have less payments than order as all orders aren't necesarily confirmed
            p.payment = get_random_instance(Payment, relation='Order')

        p.save()

    return HttpResponse('Order updated !')



def update_templatesHTML(request):
    # for slug 
    for inf in TemplateHTML.objects.all():        
        inf.save()

    return HttpResponse('TemplateHTML updated !')