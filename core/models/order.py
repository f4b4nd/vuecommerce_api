from django.db import models, IntegrityError, transaction
from django.conf import settings
from .coupon import ProductCoupon

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

    def __str__(self):
        try:
            return f"{self.user.email} - {self.ref_code}"
        except AttributeError:
            return f"{self.ref_code}"

    def get_total_price_nocharges(self):
        # No taxes, No Delivery price
        total_price = 0
        for orderproduct in self.orderproducts.all():
            total_price += orderproduct.get_final_price()
        return round(total_price, 2)

    def get_total_price(self):
        raw = self.get_total_price_nocharges()
        taxes = self.get_taxes()
        delivery = self.get_delivery_price()
        total = raw - taxes - delivery
        return total if total > 0 else 0        

    def get_taxes(self):
        # TODO : implement for real
        return 2.00

    def get_delivery_price(self):
        # TODO : implement for real
        return 5.00

class OrderProduct(models.Model):
    order = models.ForeignKey('Order',
                              on_delete=models.CASCADE,
                              related_name='orderproducts',
                              blank=True, null=True)
    product = models.ForeignKey('Product',
                                on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    # track with signals.pre_save in case of price product changes
    price = models.FloatField(blank=True, null=True)    
    class Meta:
        verbose_name_plural = 'Order__OrderProducts'

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"

    def get_sum_price_nodiscounted(self):
        # Normal price including quantities
        return self.price * self.quantity

    def get_unit_price_discounted(self):
        # Unit discount price
        coupon = ProductCoupon.objects.filter(orderproducts__pk=self.pk).first()
        if coupon:
            if coupon.amount and not coupon.percent and self.price > coupon.amount: 
                return self.price - coupon.amount
            if coupon.percent and not coupon.amount: 
                return self.price * (1- coupon.percent)
        return 0

    def get_sum_price_discounted(self):
        # Discount price including quantities
        return self.get_orderproduct_price_discount() * self.quantity

    def get_amount_saved(self):
        if self.get_unit_price_discounted() > 0:
            return self.get_sum_price_nodiscounted() - self.get_sum_price_discounted()
        return 0

    def get_final_price(self):
        if self.get_unit_price_discounted() > 0:
            return self.get_sum_price_discounted()
        else:
            return self.get_sum_price_nodiscounted()
    

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
        if self.address_type == 'S':
            order = Order.objects.filter(ship_address__pk=self.pk).first()
            return order.user

        elif self.address_type == 'B':
            order = Order.objects.filter(bill_address__pk=self.pk).first()            
            return order.user

    
    class Meta:
        verbose_name_plural = 'Order__Addresses'
        unique_together = (
            ('address_type', 'last_name', 'first_name', 'address', 'country', 'zipcode', 'city'),
        )


