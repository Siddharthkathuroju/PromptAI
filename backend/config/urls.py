"""
URL configuration for intuitive draft API.
"""
from django.contrib import admin
from django.urls import path, include

from django.urls import path, include
from api.views import api_root

urlpatterns = [
    path('', api_root), # This removes the "Not Found" error
    path('api/', include('api.urls')),
]