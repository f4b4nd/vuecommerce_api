from django.db import models, IntegrityError, transaction
from django.conf import settings


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)

    # set with signals.pre_save
    ref_code = models.CharField(max_length=30, blank=True, null=True)

    bill_address = models.ForeignKey('Address',
                                     related_name='ship_address',
                                     on_delete=models.SET_NULL,
                                     blank=True, null=True)

    ship_address = models.ForeignKey('Address',
                                     related_name='bill_address',
                                     on_delete=models.SET_NULL,
                                     blank=True, null=True)

    payment = models.ForeignKey('Payment',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)

    # Order chronology
    created_at = models.DateTimeField(auto_now_add=True) #  not necessarily paid
    expedited_at = models.DateField(default=None, null=True, blank=True)
    delivered_at = models.DateField(default=None, null=True, blank=True)
    
    # Refund
    refund_requested = models.BooleanField(default=False, null=True, blank=True)
    refund_granted = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        try:
            return f"{self.user.email} - {self.ref_code}"
        except AttributeError:
            return f"{self.ref_code}"


class OrderProduct(models.Model):
    order = models.ForeignKey('Order',
                              on_delete=models.CASCADE,
                              related_name='orderproducts',
                              blank=True, null=True)
    product = models.ForeignKey('Product',
                                on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    # set with signals.pre_save in case of price product changes
    price = models.FloatField(blank=True, null=True)    


    class Meta:
        verbose_name = 'Order__OrderProducts'

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"


class Address(models.Model):
    
    # NOTE: User is retrieved from 'Order' parent with get_user()

    CHOICES = (
        ('B', 'Bill'),
        ('S', 'Ship'),
    )

    address_type = models.CharField(max_length=1, choices=CHOICES)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    
    address = models.CharField(max_length=100)
    country = models.CharField(max_length=30)
    zipcode = models.CharField(max_length=10)
    city = models.CharField(max_length=15)

    save_info = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_user.email} - {self.address}"

    @propery
    def get_user(self):
        order = Order.objects.filter(address__pk=self.pk)
        return order.user

    
    class Meta:
        verbose_name_plural = 'Order__Address'
        unique_together = (
            ('address_type', 'user', 'address', 'country', 'zipcode', 'city'),
        )


