from django.db import models, IntegrityError, transaction
from django.conf import settings


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)

    # set with signals.pre_save
    ref_code = models.CharField(max_length=30, blank=True, null=True)

    bill_address = models.ForeignKey('Address',
                                        related_name='bill_address',
                                        on_delete=models.SET_NULL,
                                        blank=True, null=True)

    ship_address = models.ForeignKey('Address',
                                      related_name='ship_address',
                                      on_delete=models.SET_NULL,
                                      blank=True, null=True)

    payment = models.OneToOneField('Payment',
                                    on_delete=models.SET_NULL,
                                    blank=True, null=True)

    # Order chronology
    created_at = models.DateTimeField(auto_now_add=True) #  not necessarily paid
    expedited_at = models.DateField(default=None, null=True, blank=True)
    delivered_at = models.DateField(default=None, null=True, blank=True)
    
    # Refund
    refund_requested = models.BooleanField(default=False, null=True, blank=True)
    refund_granted = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        ordering = ('-created_at', )
        unique_together = (('user', 'payment', ), )

    def __str__(self):
        try:
            return f"{self.user.email} - #{self.pk} {self.ref_code}"
        except AttributeError:
            return f"{self.ref_code}"

    def get_price_nocharges(self):
        # No taxes, No Delivery price
        total = 0
        for orderproduct in self.orderproducts.all():
            total += orderproduct.get_final_price()
        return round(total, 2)

    def get_price_charges(self):
        raw = self.get_price_nocharges()
        taxes = self.get_taxes()
        delivery = self.get_delivery_price()
        total = raw + taxes + delivery
        return total if total > 0 else 0

    def get_taxes(self):
        # TODO : implement for real
        return 2.00

    def get_delivery_price(self):
        # TODO : implement for real
        return 5.00

    def get_amount_saved(self):
        # Amound saved, No taxes, No Delivery price
        cum = 0
        for orderproduct in self.orderproducts.all():
            cum += orderproduct.get_amount_saved()
        return round(cum, 2)

    def is_paid(self):
        return True if self.payment else False

    is_paid.boolean = True

class OrderProduct(models.Model):
    order = models.ForeignKey('Order',
                              on_delete=models.CASCADE,
                              related_name='orderproducts',
                              blank=True, null=True)
    product = models.ForeignKey('products.Product',
                                on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    # track current price with signals.pre_save in case of product__price changes later
    price = models.FloatField(blank=True, null=True) 
    discount_price = models.FloatField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'Order__OrderProducts'
        ordering = ('order', )
        unique_together = (('order', 'product', ), )

    def __str__(self):
        try:
            return f"#{self.pk} ({self.get_user.email} bought {self.quantity} of {self.product.title})"
        except AttributeError:
            return ""

    @property
    def get_user(self):
        try:
            return self.order.user
        except AttributeError:
            return None

    def get_sum_nodiscount(self):
        # Normal price including quantities
        return self.price * self.quantity

    def get_sum_discount(self):
        # Discount price including quantities
        return self.discount_price * self.quantity

    def get_amount_saved(self):
        if self.discount_price:
            return self.get_sum_nodiscount() - self.get_sum_discount()
        return 0

    def get_final_price(self):
        if self.discount_price:
            return self.get_sum_discount()
        return self.get_sum_nodiscount()
    

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


