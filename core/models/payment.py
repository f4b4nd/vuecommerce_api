from django.db import models, IntegrityError, transaction
from django.conf import settings
from .order import Order


class Payment(models.Model):
    # NOTE: User is retrieved from 'Order' parent with get_user()

    CHOICES = (
        ('S', 'Stripe'),
        ('P', 'Paypal'),
    )

    # id of the transaction, from stripe/paypal response 
    charge_id = models.CharField(max_length=100)

    method = models.CharField(max_length=1, choices=CHOICES, default='S')
    amount = models.FloatField()
    confirmed_at = models.DateTimeField(auto_now_add=True)    

    class Meta:
        verbose_name = 'Order__Payment'

    def __str__(self):
        try:
            return f"#{self.pk}{self.method} - {self.get_user.email} - {self.charge_id}"
        except AttributeError:
            return f"#{self.pk}{self.method} - {self.charge_id}"

    @property
    def get_user(self):
        order = Order.objects.filter(payment__pk=self.pk).first()
        return order.user


class Refund(models.Model):
    # NOTE: User is retrieved from 'Order' child with get_user()

    order = models.ForeignKey('Order',
                              on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        verbose_name = 'Order__Refund'

    def __str__(self):
        return f"{self.pk} - {self.get_user}"
    
    @property
    def get_user(self):
        return self.order.user