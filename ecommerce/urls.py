"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('accounts.urls')),
]


# ONLY WORKS WHEN settings.DEBUG, for production: use NGINX
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# DEBUG
if settings.DEBUG:

    from . import debug

    urlpatterns += [

        # generator
        path('generate-products/<int:times>', debug.generate_products, name='generate-products'),
        path('generate-orders/<int:times>', debug.generate_orders, name='generate-orders'),
        path('generate-addresses/<int:times>', debug.generate_addresses, name='generate-addresses'),
        path('generate-payments/<int:times>', debug.generate_payments, name='generate-payments'),
        path('generate-comments/<int:times>', debug.generate_comments, name='generate-comments'),       
        path('generate-categories/<int:times>', debug.generate_categories, name='generate-categories'),       
        path('generate-subcategories/<int:times>', debug.generate_subcategories, name='generate-subcategories'),       
        path('generate-product-coupons/<int:times>', debug.generate_productcoupon, name='generate-product-coupon'),      
        path('generate-order-products/<int:times>', debug.generate_orderproducts, name='generate-order-products'),      
        path('generate-refunds/<int:times>', debug.generate_refunds, name='generate-refunds'),      
        
        # updater
        path('update-users', debug.update_users, name='update-users'),
        path('update-orders', debug.update_orders, name='update-orders'),
        re_path('update-products/(?P<add_img>\w+|)', debug.update_products, name='update-products'),
        path('update-templates', debug.update_templatesHTML, name='update-templates'),
    ]
