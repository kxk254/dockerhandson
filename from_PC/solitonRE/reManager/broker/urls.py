from django.urls import path
from . import views
from django.views.generic import TemplateView


app_name = 'broker'
urlpatterns = [
    path('', views.MainView.as_view(), name='broker-list'),

    ]