from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm, CustomUserLoginForm


@login_required(login_url='player_login')
def index(request):
    return render(request, 'main/index.html')


def register_player(request):
    if request.user.is_authenticated:
        messages.warning(
            request, 'You are already logged in. Logout to create a new account.')
        return redirect('index')

    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('index')

    return render(request, 'main/register.html', {'form': form})


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
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

            messages.success(request, 'Logged in successfully')
            return redirect('index')

    return render(request, 'main/login.html', {'form': form})


@login_required(login_url='player_login')
def logout_player(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('index')
