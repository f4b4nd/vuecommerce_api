from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from . import models

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = ('slug',)


admin.site.register(models.Comment)
admin.site.register(models.ProductCoupon)
admin.site.register(models.Order)
admin.site.register(models.OrderProduct)
admin.site.register(models.Address)
admin.site.register(models.Payment)
admin.site.register(models.Refund)
admin.site.register(models.ProductCategory)
admin.site.register(models.ProductSubCategory)
admin.site.register(models.TemplateHTML)
