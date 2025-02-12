from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from users.forms import RegistrationForm, LoginForm, CreateGroupForm, AssignRoleForm
from django.contrib.auth import  login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

# test
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

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
            return redirect('dashboard')

    return render(request, "authentication/login.html", {'form':form})

@login_required
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('event-info')
    
def activate_user_account(request, user_id, token):
    user = User.objects.get(id=user_id)
    token = default_token_generator.check_token(user,token)
    if token:
        user.is_active = True
        user.save()
        return redirect('sign-in')


@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"A new group `{group.name}` has been created successful!")
        
    return render(request, 'admin/create_group.html', {'form': form})

@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {'groups': groups})

@user_passes_test(is_admin, login_url='no-permission')
def delete_group(request, id):
    group = Group.objects.get(id=id)
    if request.method == 'POST':
        group.delete()
        messages.success(request, f"Group `{group.name}` has been deleted successful!")
        return redirect('group-list')
    else:
        messages.error(request, 'Opps! Something Went Wrong! Group Delete Failed!')
        return redirect('group-list')

@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, id):
    user = User.objects.get(id=id)
    form = AssignRoleForm()
    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request, f"{user.username.upper()} you have been assign to the `{role}` role.")
            return redirect('participant')
    return render(request, 'admin/assign_role.html', {'form': form})

# No permission View
def no_permission(request):
    return render(request, 'no_permission.html')