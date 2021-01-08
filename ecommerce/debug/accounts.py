
from django.http import HttpResponse
import os, random, lorem, re, string

from . import get_random_instance, random_text

from accounts.models import User


def generate_users(request, times):
    # NOTE: passwords will not be hash correctly
    for i in range(0, times):
        u = User()
        u.email = f"{random_text('uniq', 20)}@g.com"
        u.password = random_text('t', 10).replace(' ', '')
        u.save()
    return HttpResponse(f'{times} Users created !')


def update_users(request):
    import datetime as dt
    
    for u in User.objects.all():

        if not u.last_name:
            u.last_name = random_text('t', 20)
        if not u.first_name:
            u.first_name = random_text('t', 10)
        if not u.gender:
            u.gender = str(random.randint(1, 3))
        if not u.birthdate:
            day = random.randint(1, 20)
            month = random.randint(1, 12)
            year = random.randint(1950, 2000)
            u.birthdate = dt.datetime(day=day, month=month, year=year)          
        u.save()

    return HttpResponse('Users updated !')