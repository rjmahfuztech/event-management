from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from users.forms import RegistrationForm, LoginForm, CreateGroupForm, AssignRoleForm, UpdateProfileForm, ChangePasswordForm, ResetPasswordForm, ResetPasswordConfirmForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.views.generic import ListView, CreateView, DeleteView, TemplateView, UpdateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
User = get_user_model()


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

# Class Base View for Login
class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'authentication/login.html'

    
def activate_user_account(request, user_id, token):
    user = User.objects.get(id=user_id)
    token = default_token_generator.check_token(user,token)
    if token:
        user.is_active = True
        user.save()
        return redirect('sign-in')


# Class base view for Create group
group_create_decorators = [login_required, user_passes_test(is_admin, login_url='no-permission')]
@method_decorator(group_create_decorators, name='dispatch')
class CustomCreateGroupView(CreateView):
    form_class = CreateGroupForm
    template_name = 'admin/create_group.html'
    context_object_name = 'form'
    success_url = reverse_lazy('create-group')

    def form_valid(self, form):
        group = form.save()
        messages.success(self.request, f"A new group `{group.name}` has been created successful!")
        return super().form_valid(form)

# Class base view for group list
group_list_decorators = [login_required, user_passes_test(is_admin, login_url='no-permission')]
@method_decorator(group_list_decorators, name='dispatch')
class CustomGroupListView(ListView):
    model = Group
    template_name = 'admin/group_list.html'
    context_object_name = 'groups'

    def get_queryset(self):
        queryset = Group.objects.prefetch_related('permissions').all()
        return queryset

# Class base view for delete group
group_delete_decorators = [login_required, user_passes_test(is_admin, login_url='no-permission')]
@method_decorator(group_list_decorators, name='dispatch')
class CustomGroupDeleteView(DeleteView):
    model = Group
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('group-list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        group_name = self.object.name
        self.object.delete()
        messages.success(request, f"Group `{group_name}` has been deleted successful!")
        
        return redirect(self.success_url)

@login_required
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

# User Profile
@method_decorator(login_required, name='dispatch')
class UserProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['name'] = user.get_full_name()
        context['username'] = user.username
        context['email'] = user.email
        context['designation'] = user.groups.first().name # query duplicate
        context['last_login'] = user.last_login
        context['member_since'] = user.date_joined
        context['profile_image'] = user.profile_image
        context['phone'] = user.phone
        context['bio'] = user.bio

        return context

@method_decorator(login_required, name='dispatch')
class UpdateProfileView(UpdateView):
    model = User
    context_object_name = 'form'
    template_name = 'accounts/update_profile.html'
    form_class = UpdateProfileForm

    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Your profile successfully updated.")
        return redirect('profile')

@method_decorator(login_required, name='dispatch')
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/change_password.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, "Your password has been successfully changed.")
        return super().form_valid(form)
    
class CustomPasswordResetView(PasswordResetView):
    template_name = 'authentication/reset_password.html'
    form_class = ResetPasswordForm
    success_url = reverse_lazy('sign-in')
    html_email_template_name = 'authentication/reset_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "A reset mail has been sent. Please check your E-mail.")
        return super().form_valid(form)
    
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'authentication/reset_password.html'
    form_class = ResetPasswordConfirmForm
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        messages.success(self.request, "Your password has been successfully reset.")
        return super().form_valid(form)
    
    