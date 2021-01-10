from django.http import Http404


def get_objects_or_404(Model, **kwargs):
    qs = Model.objects.filter(**kwargs)
    if not qs.exists():
        raise Http404()
    return qs


def get_object_or_create(Model, **kwargs):
    try:
        created = False
        obj = Model.objects.get(**kwargs)
    except Model.DoesNotExist:
        obj, created = Model.objects.get_or_create(**kwargs)
    return obj, created
