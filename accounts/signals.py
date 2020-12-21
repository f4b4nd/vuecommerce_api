from django.dispatch import receiver
from django.db.models import signals
from django.conf import settings
from rest_framework.authtoken.models import Token
import uuid

from .models import User


@receiver(signals.pre_save, sender=settings.AUTH_USER_MODEL)
def set_random_username(sender, instance, **kwargs):
    if not instance.username:
        instance.username = uuid.uuid4().hex[:30]


@receiver(signals.post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    # Generate a token for each user that's being created
    if created:
        Token.objects.create(user=instance)
