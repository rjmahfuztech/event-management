from django.contrib.auth.models import Permission, Group
from django.contrib.auth import get_user_model
from events.forms import StyleMixin
from django import forms
import re
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
User = get_user_model()


class RegistrationForm(StyleMixin,forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_present = User.objects.filter(email=email).exists()
        
        if email_present:
            raise forms.ValidationError('This email already exists!! Try another.')
        
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters.')
        elif not (re.search(r'[A-Z]', password) and re.search(r'[a-z]', password) and re.search(r'[0-9]', password) and re.search(r'[@#$%^&+=]', password)):
            raise forms.ValidationError('Your password must have at least 1 uppercase, 1 lowercase, 1 number and a special character.')
        
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Password do not match!! Please enter same password.')
        
        return cleaned_data


class LoginForm(StyleMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CreateGroupForm(StyleMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset= Permission.objects.prefetch_related('content_type').all(),
        required= False,
        label= 'Assign Permission',
        widget= forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']

class AssignRoleForm(StyleMixin, forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label='Select a role'    
    )

class UpdateProfileForm(StyleMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'bio', 'profile_image']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if not re.match(r'^\+?\d{9,15}$', phone):
            raise forms.ValidationError("Enter a valid phone number from 9 to 15 digits (e.g., +8801999999999, 0199999999, +1999999999).")
        
        return phone
        


class ChangePasswordForm(StyleMixin, PasswordChangeForm):
    pass

class ResetPasswordForm(StyleMixin, PasswordResetForm):
    pass

class ResetPasswordConfirmForm(StyleMixin, SetPasswordForm):
    pass