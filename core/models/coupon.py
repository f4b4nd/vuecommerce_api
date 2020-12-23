from django.db import models


class ProductCoupon(models.Model):
    code = models.CharField(max_length=15)
    product = models.OneToOneField('Product', related_name='coupon',
                                on_delete=models.SET_NULL,
                                blank=True, null=True)                            
    amount = models.FloatField(blank=True, null=True) # -10€
    percent = models.FloatField(blank=True, null=True) # -30%
    active = models.BooleanField(default=False)
    

    class Meta:
        verbose_name = 'Product__Coupon'

    def __str__(self):
        return self.code
