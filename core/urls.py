from django.urls import path, include
from rest_framework import routers

from core import api
from core import views

# HARDCODED VIEWS

urlpatterns = [
    
    path('api/informations/<slug:slug>', views.InformationView, name='Information'),
    path('api/checkout/address', api.CheckoutAddressAPI.as_view(), name='SaveAddress'),
    path('api/payment/stripe', api.StripePaymentAPI.as_view(), name='StripePayment'),
    path('api/cart', api.UpdateCartAPI.as_view(), name='UpdateCart'),
    # path('api/orders/', views.RetrieveOrderAPI.as_view(), name='retrieve-orders'),
    
]


# REST-FRAMEWORK

router = routers.DefaultRouter()
router.register(r'orders', api.OrderViewSet, basename='orders')


urlpatterns += [path('api/',  include(router.urls))]


