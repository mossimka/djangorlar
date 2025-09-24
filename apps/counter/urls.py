from django.urls import path
from . import views

app_name = 'counter'

urlpatterns = [
    path('', views.counter_view, name='counter_view'),
]