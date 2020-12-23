from django.db import models
from django.conf import settings


class Comment(models.Model):
    post = models.ForeignKey('Product',
                             on_delete=models.CASCADE,
                             related_name='comments',
                             blank=True, null=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             blank=True, null=True)

    body = models.TextField()

    rating = models.IntegerField(choices=[(i, i) for i in range(0, 6)], 
                                 blank=True, null=True)


    active = models.BooleanField(default=False, 
                                 blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Product__Comment'
        ordering = ['created_at']

    def __str__(self):
        return f"#{self.post} - #{self.user.email}"
