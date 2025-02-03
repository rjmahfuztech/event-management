from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.forms import RegistrationForm, LoginForm, CreateGroupForm
from django.contrib.auth import  login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages



# Create your views here.
def sign_up(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.is_active = False
            user.save()
            messages.success(request, 'A confirmation mail has been to you. Please check your E-Mail.')
            return redirect('sign-in')

    return render(request, "authentication/register.html", {'form': form})

def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('event-info')

    return render(request, "authentication/login.html", {'form':form})

def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')
    
def activate_user_account(request, user_id, token):
    user = User.objects.get(id=user_id)
    token = default_token_generator.check_token(user,token)
    if token:
        user.is_active = True
        user.save()
        return redirect('sign-in')


def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"A new group `{group.name}` has been created successful!")
        
    return render(request, 'admin/create_group.html', {'form': form})
