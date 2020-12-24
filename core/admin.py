from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from . import models

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = ('slug',)


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'post', 'rating', 'body')

@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('pk', 'get_user', 'address_type', 'first_name', 'last_name', 'address', 'country', 'zipcode')

    def get_user(self, obj):
        return obj.get_user.email

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_total_price', 'ref_code', 'payment',
     'bill_address', 'ship_address',  
      'created_at', 'expedited_at', 'delivered_at')

    def get_total_price(self, obj):
        return obj.get_total_price()


@admin.register(models.OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = (
        'order', 'product', 
        'price', 
        'quantity',
        'total_price',

        'unit_discount',
        'amount_saved',
        'final_price',
    )
        

    def unit_discount(self, obj):
        return obj.get_unit_price_discounted()

    def total_price(self, obj):
        return obj.get_sum_price_nodiscounted()

    def amount_saved(self, obj):
        return obj.get_amount_saved()

    def final_price(self, obj):
        return obj.get_final_price()

admin.site.register(models.ProductCoupon)
# admin.site.register(models.Order)
#admin.site.register(models.OrderProduct)
#admin.site.register(models.Address)
admin.site.register(models.Payment)
admin.site.register(models.Refund)
admin.site.register(models.ProductCategory)
admin.site.register(models.ProductSubCategory)
admin.site.register(models.TemplateHTML)
