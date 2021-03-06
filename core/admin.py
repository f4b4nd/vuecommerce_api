from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from . import models


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'user', 'is_paid',
        'total', 'amount_saved', 'no_charge', 'tax', 'delivery',
        'ref_code',
        'bill_address', 
        'created_at', 'expedited_at', 'delivered_at')

    def total(self, obj):
        return obj.get_price_charges()

    def no_charge(self, obj):
        return obj.get_price_nocharges()

    def amount_saved(self, obj):
        return obj.get_amount_saved()

    def tax(self, obj):
        return obj.get_taxes()

    def delivery(self, obj):
        return obj.get_delivery_price()


@admin.register(models.OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'order', 'product', 
        'unit_price', 
        'unit_discount',

        'quantity',
        'amount_saved',
        'final_price',
    )
        
    def unit_price(self, obj):
        return obj.price

    def unit_discount(self, obj):
        return obj.discount_price

    def amount_saved(self, obj):
        return obj.get_amount_saved()

    def final_price(self, obj):
        return obj.get_final_price()


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('pk', 'get_order', 'address_type', 'first_name', 'last_name', 'address', 'country', 'zipcode')

    def get_user(self, obj):
        try:
            return obj.get_user.email
        except AttributeError:
            return None

    def get_order(self, obj):
        return obj.get_order


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'charge_id', 'amount',  'service',)

    def user(self, obj):
        try:
            return obj.get_user.email
        except AttributeError:
            return None


@admin.register(models.Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('pk', 'order', 'accepted', 'reason')


admin.site.register(models.TemplateHTML)
