from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    return render(request, "home.html")

def event_details(request):
    return render(request, "event_details.html")