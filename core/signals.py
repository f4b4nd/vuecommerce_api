from django.dispatch import receiver
from django.db.models import signals
from django.conf import settings
from rest_framework.authtoken.models import Token
import os

from .models import Product


@receiver(signals.pre_save, sender=Product)
def on_image_delete(sender, instance, **kwargs):
    # Removes img file from media when Product.img field is removed
    
    if settings.DEFAULT_FILE_STORAGE != 'django.core.files.storage.FileSystemStorage':
        return False

    if not instance.pk:
        return False
    
    old_file = Product.objects.get(pk=instance.pk).img

    if not old_file:
        return False

    new_file = instance.img

    if  old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
    
