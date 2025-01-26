from django.shortcuts import render, redirect
from events.forms import EventModelForm,ParticipantModelForm,CategoryModelForm
from events.models import Event,Category,Participant
from django.contrib import messages
from datetime import date
from django.db.models import Count,Q


## Common Query
prefetch_query = Event.objects.prefetch_related('participant')
select_query = Event.objects.select_related('category')
# Create your views here.
def events_info(request):
    event_query = prefetch_query
    categories = Category.objects.all()
    # filter data
    get_data  = request.GET
    search_name = get_data.get('name', 'all')
    choice = get_data.get('category', 'all')
    start_date = get_data.get('start-date', 'all')
    end_date = get_data.get('end-date', 'all')

    if search_name != 'all' and choice != 'all':
        event_data = event_query.filter(name__icontains=search_name, category=choice)
    elif start_date != 'all' and end_date != 'all':
        event_data = event_query.filter(date__gte=start_date, date__lte=end_date)
    elif search_name != 'all':
        event_data = event_query.filter(name__icontains=search_name)
    elif choice != 'all':
        event_data = event_query.filter(category=choice)
    else:
        event_data = event_query.all()

    context ={
        "event_data": event_data,
        "categories": categories
    }
    return render(request, "event_info.html",context)

def event_details(request, id):
    details = prefetch_query.get(id=id)
    context ={
        "details": details
    }
    return render(request, "event_details.html",context)

def dashboard(request):
    events_query = select_query.all()
    type = request.GET.get('type', 'all')

    # filtering by date
    todays_event = events_query.filter(date=date.today())
    
    if type == 'upcoming':
        events = events_query.filter(date__gt=date.today())
    elif type == 'past':
        events = events_query.filter(date__lt=date.today())
    else:
        events = events_query.all()


    # counting
    total_participant = Participant.objects.all().count()
    count = Event.objects.aggregate(
        total_event=Count('id'),
        total_upcoming=Count('id', filter=Q(date__gt=date.today())),
        total_past=Count('id', filter=Q(date__lt=date.today())),
    )
    context ={
        "events": events,
        "todays_event": todays_event,
        "count": count,
        "total_participant": total_participant
    }
    
    return render(request, "dashboard/dashboard.html", context)

# get event
def event(request):
    events = select_query.all()
    context = {
        'events': events 
    }
    return render(request, "event.html", context)

# Event Operation
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

def update_event(request,id):
    event = Event.objects.get(id=id)
    event_form = EventModelForm(instance=event)
    
    if request.method == "POST":
        event_form = EventModelForm(request.POST, instance=event)

        if event_form.is_valid():
            event_form.save()
            messages.success(request, 'Event Updated Successful!')
            return redirect('update-event', id)

    context = {'event_form': event_form}
    return render(request, "form.html", context)

def delete_event(request, id):
    event = Event.objects.get(id=id)
    if request.method == "POST":
        event.delete()
        messages.success(request, 'Event Deleted Successful!')
        return redirect('event')
    else:
        messages.error(request, 'Opps! Something Went Wrong! Event Delete Failed!')
        return redirect('event')

# get participant
def participant(request):
    participants = Participant.objects.all()
    context={
        'participants': participants    
    }
    return render(request, "participant.html", context)

# Participant Operation
def add_participant(request):
    participant_form = ParticipantModelForm()

    if request.method == "POST":
        participant_form = ParticipantModelForm(request.POST)
        if participant_form.is_valid():
            participant_form.save()
            messages.success(request, 'Participant Added Successful!')
            return redirect('add-participant')

    context = {
        "participant_form": participant_form
    }
    return render(request, "form.html", context)

def update_participant(request,id):
    participant = Participant.objects.get(id=id)
    participant_form = ParticipantModelForm(instance=participant)

    if request.method == "POST":
        participant_form = ParticipantModelForm(request.POST, instance=participant)

        if participant_form.is_valid():
            participant_form.save()
            messages.success(request, "Participant Updated Successful!")
            return redirect('update-participant', id)
    
    context = {'participant_form': participant_form}
    return render(request, "form.html", context)

def delete_participant(request,id):
    participant = Participant.objects.get(id=id)
    if request.method == "POST":
        participant.delete()
        messages.success(request, "Participant Deleted Successful!")
        return redirect('participant')
    else:
        messages.error(request, 'Opps! Something Went Wrong! Participant Delete Failed!')
        return redirect('participant')

# get category
def category(request):
    categories = Category.objects.all()
    context={
        'categories': categories    
    }
    return render(request, "category.html", context)

# Category Operation
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

def update_category(request,id):
    category = Category.objects.get(id=id)
    category_form = CategoryModelForm(instance=category)

    if request.method == "POST":
        category_form = CategoryModelForm(request.POST, instance=category)

        if category_form.is_valid():
            category_form.save()
            messages.success(request, "Category Updated Successful!")
            return redirect('update-category', id)
        
    context = {"category_form": category_form}
    return render(request, "form.html", context)

def delete_category(request,id):
    category = Category.objects.get(id=id)

    if request.method == "POST":
        category.delete()
        messages.success(request, "Category Deleted Successful!")
        return redirect('category')
    else:
        messages.success(request, 'Opps! Something Went Wrong! Event Delete Failed!')
        return redirect('category')