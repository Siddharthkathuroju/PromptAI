"""
URL configuration for intuitive draft API.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('api.urls')),
]
