from django.http import HttpResponse
from django.shortcuts import redirect, render
from bike_rental.settings import DEFAULT_FROM_EMAIL
from .forms import RegisterForm, ResetPasswordForm
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import EmailConfirmation
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ChangePasswordForm
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                
                code = get_random_string(length=22)
                EmailConfirmation.objects.create(user=user, code=code)
                
                activation_link = request.build_absolute_uri(
                    reverse('confirm_email', args=[code])
                )
                
                send_mail(
                    'Confirm your account',
                    f'Click the link to confirm your account: {activation_link}',
                    DEFAULT_FROM_EMAIL,
                    [form.cleaned_data['email']],
                    fail_silently=False,
                )
                
                return render(request, 'email_confirm.html')
            
            except Exception as e:
                print(f"Error: {e}")
                form.add_error(None, '')
        else:
            form.add_error(None, 'Please correct mistakes')
    
    else:
        form = RegisterForm()
    
    return render(request, "register.html", {'form': form})


def confirm_email_view(request, code):
    try:
        conf = EmailConfirmation.objects.get(code=code)
        conf.is_confirmed = True
        conf.user.is_active = True
        conf.user.save()
        conf.save()
        return render(request, 'email_confirmed.html', {})
    except EmailConfirmation.DoesNotExist:
        return HttpResponse("Error.")
    

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            conf = EmailConfirmation.objects.filter(user=user).first()
            if conf and conf.is_confirmed:
                login(request, user)
                return redirect('home')
            else:
                return render(request, "confirm_email.html", {})
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {'form': form})

@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request) 
        return redirect('home') 
    return render(request, "logout.html") 

@login_required
def delete_account_view(request):
    if request.method == "POST":
        EmailConfirmation.objects.filter(user=request.user).delete()

        code = get_random_string(length=64)
        EmailConfirmation.objects.create(user=request.user, code=code)

        send_mail(
            'Confirm Account Deletion',
            f'Click the link to delete your account: '
            f'http://127.0.0.1:8000/confirm_delete/{code}/',
            'fake@mail.com',
            [request.user.email],
            fail_silently=False,
        )

        return render(request, 'confirm_delete_view.html', {})
    return render(request, 'delete_account.html')

def confirm_delete_view(request, code):
    conf = EmailConfirmation.objects.filter(code=code, is_confirmed=False).first()

    if conf:
        conf.is_confirmed = True
        conf.save()
        user = conf.user
        user.delete() 
        logout(request)
        return HttpResponse("Your account has been deleted.")
    return HttpResponse("")

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password'] 
            user = request.user
            user.set_password(new_password) 
            user.save()
            update_session_auth_hash(request, user)
            return redirect('user')
    else:
        form = ChangePasswordForm(user=request.user)

    return render(request, 'change_password.html', {'form': form})


def reset_password_view(request, code):
    try:
        conf = EmailConfirmation.objects.get(code=code, is_confirmed=False)
    except EmailConfirmation.DoesNotExist:
        return HttpResponse("Invalid or expired reset code.")

    if request.method == 'POST':
        form = ResetPasswordForm(user=conf.user, data=request.POST)  
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user = conf.user

            user.set_password(new_password)
            user.save()

            update_session_auth_hash(request, user)
            login(request, user)
            
            conf.is_confirmed = True
            conf.save()
            return redirect('home') 
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ResetPasswordForm(user=conf.user) 

    return render(request, 'reset_password.html', {'form': form})

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            existing_confirmation = EmailConfirmation.objects.filter(user=user).first()

            code = get_random_string(length=64)
            existing_confirmation.code = code 
            existing_confirmation.is_confirmed = False
            existing_confirmation.save()

            send_mail(
                'Reset your password',
                f'Click the link to reset your password: http://127.0.0.1:8000/reset_password/{code}/',
                'fake@mail.com',
                [email],
                fail_silently=False,
            )


            return render(request, "check_email_to_confirm.html", {})

        except User.DoesNotExist:
            return render(request, "no_user_found.html", {})
    return render(request, 'forgot_password.html')