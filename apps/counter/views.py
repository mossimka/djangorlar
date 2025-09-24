from django.shortcuts import render

# Create your views here.
def counter_view(request):
    return render(request, 'counter.html')