from django.dispatch import receiver
from django.db.models import signals
from django.conf import settings
from rest_framework.authtoken.models import Token
import os, uuid

from .models import Product, Order, OrderProduct, ProductCoupon


@receiver(signals.pre_save, sender=Product)
def on_product_img_delete(sender, instance, **kwargs):
    # Removes img file from media when Product.img field is removed

    if settings.DEFAULT_FILE_STORAGE != 'django.core.files.storage.FileSystemStorage':
        return False

    if not instance.pk:
        return False
    
    old_img_file = Product.objects.get(pk=instance.pk).img

    if not old_img_file:
        return False

    new_img_file = instance.img

    if  old_img_file != new_img_file:
        if os.path.isfile(old_img_file.path):
            os.remove(old_img_file.path)
    

@receiver(signals.pre_save, sender=Order)
def on_order_save(sender, instance, **kwargs):
    # sets ref_code

    if not instance.ref_code:
        instance.ref_code = uuid.uuid4().hex[:30]
    

@receiver(signals.pre_save, sender=OrderProduct)
def on_orderproduct_save(sender, instance, **kwargs):
    # tracks current price in case of it changes later
    
    curr_price = instance.product.price
    curr_disc_price = 0

    if not instance.price:
        instance.price = curr_price
    
    if not instance.discount_price:
        c = ProductCoupon.objects.filter(product__pk=instance.product.pk).first()
        if not c:
            return
        elif c.active and c.amount and not c.percent: 
            curr_disc_price = curr_price - c.amount
        elif c.active and c.percent and not c.amount: 
            curr_disc_price = curr_price * (1- (c.percent / 100))

        instance.discount_price = curr_disc_price if curr_disc_price > 0 else 0
