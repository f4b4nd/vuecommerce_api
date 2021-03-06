from django.db import models


class ProductCoupon(models.Model):
    code = models.CharField(max_length=15)
    product = models.ForeignKey('Product', 
                                related_name='coupons',
                                on_delete=models.SET_NULL,
                                blank=True, null=True)                            
    amount = models.FloatField(blank=True, null=True) # -10€
    percent = models.FloatField(blank=True, null=True) # -30%
    active = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Coupon'

    def __str__(self):
        minus = f"-{self.amount}EUR" if self.amount else f"-{self.percent}%"
        return f"#{self.pk} - {self.code} {minus} (product {self.product})"