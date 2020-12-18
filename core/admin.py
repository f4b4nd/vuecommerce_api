from django.contrib import admin
from .models import Product, Information

class ProductAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    # prepopulated_fields = {"slug": ("title",)}


admin.site.register(Product, ProductAdmin)
admin.site.register(Information)
