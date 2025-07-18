from django.shortcuts import render, redirect
from events.forms import EventModelForm,CategoryModelForm
from events.models import Event,Category
from django.contrib import messages
from datetime import date
from django.db.models import Count,Q
from django.utils.dateformat import DateFormat
from django.db.models.functions import TruncMonth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from users.views import is_admin
from django.views.generic import DetailView, UpdateView
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
User = get_user_model()

# Test
def is_organizer_or_admin(user):
    return user.groups.filter(Q(name='Organizer') | Q(name='Admin')).exists()

## Common Query
event_optimized_query = Event.objects.select_related('category').prefetch_related('participant').all().order_by('id')
# Create your views here.
def events_info(request):
    event_query = event_optimized_query

    context ={
        "limited_event": event_query.order_by('id')[:6],
    }
    return render(request, "event_info.html",context)

def event_list(request):
    event_query = event_optimized_query
    categories = Category.objects.all()

    # filter data
    get_date = request.GET
    search_by_name = get_date.get('name', '').strip()
    choices = get_date.get('category', '').strip()
    start_date = get_date.get('start_date', '').strip()
    end_date = get_date.get('end_date', '').strip()
    
    # for safely filter
    filters = {}

    if search_by_name:
        filters['name__icontains'] = search_by_name
    if choices:
        filters['category'] = choices
    if start_date and end_date:
        try:
            filters['date__range'] = [start_date, end_date]
        except:
            pass # if invalid date format comes then ignore.

    event_data = event_query.filter(**filters);

    # Pagination
    paginator = Paginator(event_data, 6)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    # Remove `page` param and build query string
    querydict = request.GET.copy()
    if 'page' in querydict:
        querydict.pop('page')
    query_string = querydict.urlencode()

    context ={
        "categories": categories,
        "page_obj": page_object,
        # "get_data": get_date,
        "query_string": query_string
    }
    return render(request, "event_list.html", context)


# Class base view for event details
class CustomEventDetailsView(DetailView):
    model = Event
    template_name = 'event_details.html'
    pk_url_kwarg = 'id'
    context_object_name = 'details'

    def get_queryset(self):
        return Event.objects.prefetch_related('participant')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_event = self.object

        # get related events that are in same category and exclude current event
        related_events = Event.objects.filter(category=current_event.category).exclude(id=current_event.id)

        context['related_events'] = related_events
        return context
        

@login_required
def dashboard(request):
    events_query = event_optimized_query
    type = request.GET.get('type', 'all')

    # filtering by date
    todays_event = events_query.filter(date=date.today())
    
    if type == 'upcoming':
        events = events_query.filter(date__gt=date.today())
    elif type == 'past':
        events = events_query.filter(date__lt=date.today())
    else:
        events = events_query

    # for bar chart
    event_by_month = (
        Event.objects.annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    months = []
    event_counts = []

    for item in event_by_month:
        month = item['month']
        month_name = DateFormat(month).format('M') # example: 'Jan', 'Feb', etc...
        months.append(month_name)
        event_counts.append(item['count'])
    
    # for pie chart
    categories_with_event = Category.objects.prefetch_related('event').all()

    categories = []
    category_event_count = []

    for category in categories_with_event:
        categories.append(category.name)
        if category.event.count() >= 1:
            category_event_count.append(category.event.count())
        else:
            category_event_count.append(0)

    # pagination
    paginator = Paginator(events, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Remove `page` param and build query string
    querydict = request.GET.copy()
    if 'page' in querydict:
        querydict.pop('page')
    query_string = querydict.urlencode()

    # counting
    total_participant = User.objects.all().count()
    count = Event.objects.aggregate(
        total_event=Count('id'),
        total_upcoming=Count('id', filter=Q(date__gt=date.today())),
        total_past=Count('id', filter=Q(date__lt=date.today())),
    )
    context ={
        "months": months,
        "event_counts": event_counts,
        "categories": categories,
        "category_event_count": category_event_count,
        "page_obj": page_obj,
        "query_string": query_string,
        "todays_event": todays_event,
        "count": count,
        "total_participant": total_participant
    }
    
    return render(request, "dashboard/dashboard.html", context)

# get event
@login_required
@user_passes_test(is_organizer_or_admin, login_url='no-permission')
def event(request):
    events = event_optimized_query

    # pagination
    paginator = Paginator(events, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj 
    }
    return render(request, "event.html", context)

# Event Operation
@login_required
@user_passes_test(is_organizer_or_admin, login_url='no-permission')
def add_event(request):
    event_form = EventModelForm()

    if request.method == "POST":
        event_form = EventModelForm(request.POST, request.FILES)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, 'Event Added Successful!')
            return redirect('add-event')

    context = {
        "event_form": event_form
    }
    return render(request, "form.html", context)


# Class base view for update event
event_update_decorators = [login_required, user_passes_test(is_organizer_or_admin, login_url='no-permission')]
@method_decorator(event_update_decorators, name='dispatch')
class CustomUpdateEventView(UpdateView):
    model = Event
    form_class = EventModelForm
    pk_url_kwarg = 'id'
    template_name = 'form.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_form'] = self.get_form()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        event_form = EventModelForm(request.POST, request.FILES, instance=self.object)

        if event_form.is_valid():
            event_form.save()
            messages.success(request, 'Event Updated Successful!')
            return  redirect('update-event', self.object.id)
        else:
            messages.error(request, 'Opps!! Something went wrong please try again!')
            return  redirect('update-event', self.object.id)
    

@login_required
@user_passes_test(is_organizer_or_admin, login_url='no-permission')
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
@login_required
@user_passes_test(is_admin, login_url='no-permission')
def participant(request):
    participants = User.objects.all()
    context={
        'participants': participants    
    }
    return render(request, "participant.html", context)

@login_required
def join_in_event(request, id):
    event = Event.objects.get(id=id)
    is_added = event.participant.filter(id=request.user.id).exists()
    if is_added == False:
        event.participant.add(request.user)
        messages.success(request, f"You are successfully booked this `{event.name}` event.")
        return redirect('my-event')
    else:
        return redirect('event-info')
    
@login_required
def user_booked_events(request):
    user_events = Event.objects.filter(participant=request.user).select_related('category')
    return render(request, "user_booked_event.html", {'user_events': user_events})
        

@login_required
@user_passes_test(is_admin, login_url='no-permission')
def delete_participant(request,id):
    participant = User.objects.get(id=id)
    if request.method == "POST":
        # this 3 user can't delete. because it's important for test
        if participant.username == 'admin' or 'organizer' or 'user':
            messages.error(request, f"You can't delete '{participant.first_name + " " + participant.last_name}'. This user is important!")
            return redirect('participant')
        
        participant.delete()
        messages.success(request, "Participant Deleted Successful!")
        return redirect('participant')
    else:
        messages.error(request, 'Opps! Something Went Wrong! Participant Delete Failed!')
        return redirect('participant')

# get category
@login_required
@user_passes_test(is_organizer_or_admin, login_url='no-permission')
def category(request):
    categories = Category.objects.all()
    context={
        'categories': categories    
    }
    return render(request, "category.html", context)

# Category Operation
@login_required
@user_passes_test(is_organizer_or_admin, login_url='no-permission')
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

@login_required
@user_passes_test(is_organizer_or_admin, login_url='no-permission')
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

@login_required
@user_passes_test(is_organizer_or_admin, login_url='no-permission')
def delete_category(request,id):
    category = Category.objects.get(id=id)

    if request.method == "POST":
        category.delete()
        messages.success(request, "Category Deleted Successful!")
        return redirect('category')
    else:
        messages.error(request, 'Opps! Something Went Wrong! Event Delete Failed!')
        return redirect('category')