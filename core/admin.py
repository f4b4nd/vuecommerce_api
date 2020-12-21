from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from core.models import Product, Information

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = ('slug',)


admin.site.register(Information)
