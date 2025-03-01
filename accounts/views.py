from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm
from django.http import JsonResponse
from .models import CustomUser

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'exists': CustomUser.objects.filter(username=username).exists()
    }
    return JsonResponse(data)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Неверный логин или пароль."
    return render(request, 'accounts/login.html', {'error_message': error_message})

def user_logout(request):
    logout(request)
    return redirect('home')
