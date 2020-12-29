from django.urls import path, include
from rest_framework import routers

from core import api
from core import views

# HARDCODED VIEWS

urlpatterns = [
    
    path('api/informations/<slug:slug>', views.InformationView, name='Information'),
    path('api/save-address', api.SaveAddressAPI.as_view(), name='SaveAddress'),
    # path('api/orders/', views.RetrieveOrderAPI.as_view(), name='retrieve-orders'),
    
]


# REST-FRAMEWORK

router = routers.DefaultRouter()
router.register(r'products', api.ProductViewSet, basename='products')
router.register(r'topics', api.ProductTopicViewSet, basename='topics')
router.register(r'orders', api.OrderViewSet, basename='orders')


urlpatterns += [path('api/',  include(router.urls))]


