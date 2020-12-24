from django.urls import path, include
from rest_framework import routers

from core import views


# HARDCODED VIEWS

urlpatterns = [
    
    path('api/informations/<slug:slug>', views.InformationView, name='Information'),
    # path('api/orders/', views.RetrieveOrderAPI.as_view(), name='retrieve-orders'),
    
]


# REST-FRAMEWORK

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='products')
router.register(r'orders', views.OrderViewSet, basename='orders')
router.register(r'comments', views.CommentViewSet, basename='comments')

urlpatterns += [path('api/',  include(router.urls))]


