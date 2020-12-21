from django.dispatch import receiver
from django.db.models import signals
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify
import uuid

from .models import User


@receiver(signals.pre_save, sender=User)
def set_random_username(sender, instance, **kwargs):    
    if not instance.username:
        instance.username = uuid.uuid4().hex[:30]
