from django.urls import path

from .views import ats_view

urlpatterns = [
    path("ats-check/", ats_view, name="ats_check"),
]
