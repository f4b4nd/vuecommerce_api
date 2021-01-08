from django.db import models, IntegrityError, transaction
from django.utils.text import slugify
from django.conf import settings

from . import ProductCoupon


class Product(models.Model):

    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    resume = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    img = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        try:
            with transaction.atomic():
                self.slug = slugify(self.title)
                super().save(*args, **kwargs)
        except IntegrityError:
            self.slug = f"{slugify(self.title)}-{self.id}"
            super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.pk} - {self.title}"

    def get_groups(self):
        groups = ProductGroups.objects.filter(products__pk=self.pk)
        return groups

    def get_discount_price(self):
        c = ProductCoupon.objects.filter(product__pk=self.pk).first()
        if not c:
            return ''
        elif c.active and c.amount and not c.percent: 
            return self.price - c.amount
        elif c.active and c.percent and not c.amount: 
            return self.price * (1- (c.percent / 100))
        return ''

    def get_coupon(self):
        c = ProductCoupon.objects.filter(product__pk=self.pk).first()
        return f"#{c.pk} {c.code}" if c else ''


class ProductGroups(models.Model):
    """
    (ProductGroups, Product) = (n, n)
    (ProductGroups, Topic) = (n, 1)
    Ex:
    - Product "Huile de coco" -> in Groups [huiles de beauté, huile de cuisine]
    - Group "Huile de beauté" -> in Topic "Beauté"
    - Group "Huile de Cuisine" -> in Topic "Cuisine"

    -> Limit topics to a reasonable number of instances (ex: 10)
    -> Groups are unlimited 
    """

    name = models.CharField(unique=True, max_length=80)
    slug = models.SlugField(unique=True, blank=True, null=True)

    products = models.ManyToManyField('Product',
                                      related_name='groups',
                                      #on_delete=models.SET_NULL, 
                                      blank=True)

    topic = models.ForeignKey('ProductTopic',
                               related_name='groups', 
                               on_delete=models.SET_NULL,
                               blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Product__Groups'

    def __str__(self):
        return f"#{self.pk} - {self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_products(self):
        # manytomany for admin 
        products = [f"(#{p.pk} {p.title})" for p in self.products.all()]
        return products


class ProductTopic(models.Model):

    name = models.CharField(unique=True, max_length=80)
    slug = models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Product__Topic'

    def __str__(self):
        return f"#{self.pk} - {self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_groups(self):
        groups = ProductGroups.objects.filter(topic__pk=self.pk)        
        return groups

