from django.urls import path
from .views import AnalyzePlanView, health_check

urlpatterns = [
    path('health/', health_check, name='health-check'),
    path('analyze-plan/', AnalyzePlanView.as_view(), name='analyze-plan'),
]
