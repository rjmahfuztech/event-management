from django.shortcuts import render, HttpResponse
from events.forms import EventModelForm

# Create your views here.
def home(request):
    return render(request, "home.html")

def event_details(request):
    return render(request, "event_details.html")

def dashboard(request):
    return render(request, "dashboard/dashboard.html")

def add_event(request):
    event_form = EventModelForm()

    context = {
        "event_form": event_form
    }

    return render(request, "event_form.html", context)