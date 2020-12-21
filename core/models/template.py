from django.db import models, IntegrityError, transaction
from django.utils.text import slugify


class TemplateHTML(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.title}"

    def save(self, *args, **kwargs):
        try:
            with transaction.atomic():
                self.slug = slugify(self.title)
                super().save(*args, **kwargs)
        except IntegrityError:
            self.slug = f"{slugify(self.title)}-{self.id}"
            super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Templates HTML'