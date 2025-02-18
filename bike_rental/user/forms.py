from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from .models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    date = forms.DateField(required=True, widget=forms.SelectDateWidget(years=range(1950, timezone.now().year)))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'date']

    def clean_date(self):
        date = self.cleaned_data.get('date')
        today = timezone.now().date()
        age = today.year - date.year - ((today.month, today.day) < (date.month, date.day))
        if age < 16:
            raise forms.ValidationError("You must be at least 16 years old to register.")
        return date

class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput, label='New Password', min_length=6)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password', min_length=6)

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Old Password")
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password")

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("New passwords are not the same")
        
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Old password is incorrect")
        return cleaned_data