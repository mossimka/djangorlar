from django import http
from django.shortcuts import render


def home_view(request: http.request) -> http.HttpResponse:
    return render(request, 'home.html')