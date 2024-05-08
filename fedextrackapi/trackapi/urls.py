
from django.contrib import admin
from django.urls import path
from trackapi.views import FedexTrackingView
from . import views

urlpatterns = [
    path('track/', FedexTrackingView.as_view()),
]
