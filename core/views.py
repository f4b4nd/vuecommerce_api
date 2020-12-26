
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.views.decorators.http import require_http_methods

from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication

from . import models as core_models 
from . import serializers as core_serializers


@require_http_methods(["GET"])
def InformationView(request, slug):
    obj = get_object_or_404(core_models.TemplateHTML, slug=slug)
    serialized_obj = serializers.serialize('json', [ obj, ], ensure_ascii=False)
    status = 200
    return JsonResponse(serialized_obj[1:-1], safe=False)
