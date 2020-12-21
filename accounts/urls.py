from django.urls import path, include
from .api import RegisterAPI, LoginAPI, UserAPI, LogoutAPI


urlpatterns = [

    path('api/auth/register', RegisterAPI.as_view(),  name='register'),
    path('api/auth/login', LoginAPI.as_view(), name='login'),
    path('api/auth/logout', LogoutAPI.as_view(), name='logout'),

    path('api/auth/user', UserAPI.as_view()),

]