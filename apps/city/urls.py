from django.urls import path
from . import views

app_name = 'city'

urlpatterns = [
    path('', views.city_view, name='city_view'),
]