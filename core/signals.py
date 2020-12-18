from django.dispatch import receiver
from django.db.models import signals
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify

from core.models import Product


@receiver(signals.pre_save, sender=Product)
def pre_save_for_conference_code_fixture(sender, instance, **kwargs):
    """
    Automatically add created_at when loaddata
    """
    if kwargs['raw']:
        instance.created_at = timezone.now()
