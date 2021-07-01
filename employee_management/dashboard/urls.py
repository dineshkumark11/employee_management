from django.urls import path
from .views import report

urlpatterns = [
    path("", report, name="report"),
]
