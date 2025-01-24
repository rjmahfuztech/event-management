from django.shortcuts import render, HttpResponse, redirect
from events.forms import EventModelForm,ParticipantModelForm,CategoryModelForm
from events.models import Event,Category,Participant
from django.contrib import messages

# Create your views here.
def events(request):
    event_data = Event.objects.all()
    context ={
        "event_data": event_data
    }
    return render(request, "events.html",context)

def event_details(request, id):
    details = Event.objects.get(id=id)
    context ={
        "details": details
    }
    return render(request, "event_details.html",context)

def dashboard(request):
    events = Event.objects.all()
    context ={
        "events": events
    }
    return render(request, "dashboard/dashboard.html", context)

def add_event(request):
    event_form = EventModelForm()

    if request.method == "POST":
        event_form = EventModelForm(request.POST)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, 'Event Added Successful!')
            return redirect('add-event')

    context = {
        "event_form": event_form
    }
    return render(request, "form.html", context)

def add_participant(request):
    participant_form = ParticipantModelForm()

    if request.method == "POST":
        participant_form = ParticipantModelForm(request.POST)
        if participant_form.is_valid():
            participant_form.save()
            messages.success(request, 'One Participant Added Successful!')
            return redirect('add-participant')

    context = {
        "participant_form": participant_form
    }
    return render(request, "form.html", context)

def add_category(request):
    category_form = CategoryModelForm()

    if request.method == "POST":
        category_form = CategoryModelForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            messages.success(request, 'Category Created Successful!')
            return redirect('add-category')

    context = {
        "category_form": category_form
    }
    return render(request, "form.html", context)