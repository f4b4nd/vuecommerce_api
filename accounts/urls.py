from django.urls import path, include
from . import api

urlpatterns = [

    path('api/auth/register', api.RegisterAPI.as_view(),  name='register'),
    path('api/auth/login', api.LoginAPI.as_view(), name='login'),
    path('api/auth/logout', api.LogoutAPI.as_view(), name='logout'),

    path('api/auth/user', api.ExampleUserAPI.as_view()),

]