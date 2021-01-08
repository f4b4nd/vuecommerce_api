from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from . import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'title',
        'price', 'get_discount_price',
        'get_coupon', 'get_groups',
    )
    exclude = ('slug',)

    def get_groups(self, obj):
        groups = [f"(#{g.pk} {g.name})" for g in obj.get_groups()]
        return groups

    def get_coupon(self, obj):
        return obj.get_coupon()


@admin.register(models.ProductGroups)
class ProductGroupsAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'topic', 'get_products', )

    def get_name(self, obj):
        return f"#{obj.pk} {obj.name}"


@admin.register(models.ProductTopic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'get_groups', )

    def get_name(self, obj):
        return f"#{obj.pk} {obj.name}"

    def get_groups(self, obj):
        groups = [f"(#{g.pk} {g.name})" for g in obj.get_groups()]
        return groups


@admin.register(models.ProductCoupon)
class ProductCouponAdmin(admin.ModelAdmin):
    list_display = ('get_code','active', 'product', 'amount',  'percent', )

    def get_code(self, obj):
        return f"#{obj.pk} {obj.code}"


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'post', 'rating', 'body')