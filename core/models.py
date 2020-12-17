from django.db import models

class Product(models.Model):

    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    resume = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    img = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.pk} - {self.title}"