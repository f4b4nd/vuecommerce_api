from django.db import models, IntegrityError, transaction
from django.conf import settings


class Comment(models.Model):
    post = models.ForeignKey('Product',
                             on_delete=models.CASCADE,
                             related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    body = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(0, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Product__Comment'
        ordering = ['created_at']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.user.email)
