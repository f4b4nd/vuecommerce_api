from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import Product, Information, User

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = ('slug',)


# admin.site.register(Product, ProductAdmin)
admin.site.register(Information)
admin.site.register(User)