from django.dispatch import receiver
from django.db.models import signals
from django.contrib.auth import get_user_model
from django.utils.text import slugify
"""
# from core.models import Product


@receiver(signals.pre_save, sender=Product)
def populate_slug(sender, instance, **kwargs):
    instance.slug = slugify(instance.title)


def autoslug(fieldname):
    def decorator(model):
        # some sanity checks first
        assert hasattr(model, fieldname), f"Model has no field {fieldname!r}"
        assert hasattr(model, "slug"), "Model is missing a slug field"

        @receiver(signals.pre_save, sender=model)
        def generate_slug(sender, instance, *args, raw=False, **kwargs):
            if not raw and not instance.slug:
                source = getattr(instance, fieldname)
                slug = slugify(source)
                if slug:  # not all strings result in a slug value
                    instance.slug = slug
        return model
    return decorator
"""