from django.dispatch import receiver
from django.db.models import signals
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify
import uuid

from .models import User


def gen_random_username():
    return uuid.uuid4().hex[:30]


@receiver(signals.pre_save, sender=User)
def pre_save_for_conference_code_fixture(sender, instance, **kwargs):
    """
    Automatically add created_at when loaddata
    """
    if not instance.username:
        instance.username = gen_random_username()
