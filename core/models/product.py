from django.db import models, IntegrityError, transaction
from django.utils.text import slugify
from django.conf import settings

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


class ProductGroups(models.Model):

    name = models.CharField(unique=True, max_length=80)
    slug = models.SlugField(unique=True, blank=True, null=True)

    products = models.ManyToManyField('Product',
                                      related_name='groups',
                                      #on_delete=models.SET_NULL, 
                                      blank=True)

    topic = models.ForeignKey('Topic',
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
        products = [f"#{p.pk} {p.title} " for p in self.products.all()]
        return "\n".join(products)

    # def get_products(self):
    #     return Product.objects.filter(category__pk=self.pk)

class Topic(models.Model):

    name = models.CharField(unique=True, max_length=80)
    slug = models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Product__Topic'

    def __str__(self):
        return f"#{self.pk} - {self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)