from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.utils.encoding import (force_text)
from django.utils.http import urlsafe_base64_decode

from .models import Place
from .forms import CustomUserCreationForm, CustomUserLoginForm
from .utils import account_activation_email_preparation, send_email_using_ses, welcome_email


def handler404(request, exception):
    messages.error(request, 'Requested page not found.')
    return redirect('index')


def handler500(request):
    return render(request, 'main/500.html', status=500)


@login_required(login_url='player_login')
def index(request):
    temp_list = []
    import random
    total = random.randint(13, 23)
    for i in range(total):
        place = Place.objects.order_by('?').first()
        temp_list.append(place)

    paginator = Paginator(temp_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'temp_list': temp_list,
        'page_obj': page_obj,
    }

    return render(request, 'main/index.html', context=context)


def register_player(request):
    if request.user.is_authenticated:
        messages.warning(
            request, 'You are already logged in. Logout to create a new account.')
        return redirect('index')

    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # send verification email
            email_data = account_activation_email_preparation(request, user)

            email_status = send_email_using_ses(
                user.email, "Activate your account", email_data)

            if not email_status:
                user.delete()
                messages.error(
                    request, 'There was an error sending the activation email. Please try again.')
                return redirect('player_register')

            messages.success(
                request, 'Account created successfully!\nPlease check your email and verify.')

            return redirect('player_register')
        else:
            error_dict = dict(form.errors.items())
            if "captcha" in error_dict:
                messages.error(
                    request, 'Please confirm you are not a robot.')

    return render(request, 'main/register.html', {'form': form})


def verify_activation_url(request, uidb64, token):
    try:
        user_id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)

        if user.is_active:
            return redirect("player_login")

        user.is_active = True
        user.save()
        messages.success(
            request, "Account activated successfully. Please login!")
        return redirect("player_login")

    except:
        messages.error(request, "Invalid activation link")
        return redirect("player_register")


def login_player(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.')
        return redirect('index')

    form = CustomUserLoginForm()

    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username,
                                password=password)

            if user.last_login is None:
                email_data = welcome_email(user)
                email_status = send_email_using_ses(
                    user.email, "Welcome to Weekly Football!", email_data)

                if not email_status:
                    messages.error(
                        request, 'There was an error sending the welcome email.')

            if user is not None:
                login(request, user)

            messages.success(request, 'Logged in successfully')
            return redirect('index')

    return render(request, 'main/login.html', {'form': form})


@ login_required(login_url='player_login')
def logout_player(request):
    logout(request)
    messages.warning(request, 'Logged out successfully')
    return redirect('index')


@ login_required(login_url='player_login')
def about(request):
    return render(request, 'main/about.html')


@ login_required(login_url='player_login')
def player_profile(request):
    user = User.objects.get(username=request.user.username)
    context = {
        'user': user,
    }
    return render(request, 'main/profile.html', context=context)
