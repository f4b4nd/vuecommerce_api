from django.db import models, IntegrityError, transaction
from django.utils.text import slugify


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
                super(Product, self).save(*args, **kwargs)
        except IntegrityError:
            self.slug = f"{slugify(self.title)}-{self.id}"
            super(Product, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.pk} - {self.title}"
