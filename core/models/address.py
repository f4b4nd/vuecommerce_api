from django.db import models, IntegrityError, transaction
from django.conf import settings

from . import Order


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
        try:
            return f"#{self.pk}{self.address_type} - {self.get_user.email} - {self.address}"
        except AttributeError:
            return f"#{self.pk}{self.address_type} - {self.address}"

    @property
    def get_user(self):
        if self.get_order:
            return self.get_order.user

    @property
    def get_order(self):
        if self.address_type == 'S':
            order = Order.objects.filter(ship_address__pk=self.pk).first()
            return order

        elif self.address_type == 'B':
            order = Order.objects.filter(bill_address__pk=self.pk).first()            
            return order

    
    class Meta:
        verbose_name_plural = 'Order__Addresses'
        ordering = ('-created_at',)
        unique_together = (
            ('address_type', 'last_name', 'first_name', 'address', 'country', 'zipcode', 'city'),
        )
