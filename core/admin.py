from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from . import models

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'price', 'category', 'created_at',)
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
    list_display = (
        'user', 'is_paid',
        'total', 'no_charge', 'tax', 'delivery',
        'ref_code',
        'bill_address', 
        'created_at', 'expedited_at', 'delivered_at')

    def total(self, obj):
        return obj.get_total_price()

    def no_charge(self, obj):
        return obj.get_total_price_nocharges()

    def is_paid(self, obj):
        return obj.is_paid()


    def tax(self, obj):
        return obj.get_taxes()

    def delivery(self, obj):
        # TODO : implement for real
        return obj.get_delivery_price()


@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'products', 'subcategories')

    def subcategories(self, obj):
        return obj.subcategories

    def products(self, obj):
        products = [ f"(#{p.pk} {p.title})" for p in obj.get_products()]
        return products


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'charge_id', 'amount',  'method',)

    def user(self, obj):
        return obj.get_user.email


@admin.register(models.ProductCoupon)
class ProductCouponAdmin(admin.ModelAdmin):
    list_display = ('pk', 'code', 'product', 'amount',  'percent', 'active',)

    def user(self, obj):
        return obj.get_user.email

@admin.register(models.ProductSubCategory)
class ProductSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'parent')



@admin.register(models.OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'order', 'product', 
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


@admin.register(models.Refund)
class ProductSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'order', 'accepted', 'reason')


admin.site.register(models.TemplateHTML)
