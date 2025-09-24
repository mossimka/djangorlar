from django.utils import timezone
from django.shortcuts import render

# Create your views here.
def city_view(request):
    current_time = timezone.now()
    context = {
        'city': 'UTC',
        'current_time': current_time,
    }
    return render(request, 'city.html', context)