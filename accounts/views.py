from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm
from django.http import JsonResponse
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

@login_required
def profile(request):
    error = None
    user = request.user
    if request.method == "POST":
        new_username = request.POST.get('username', '').strip()
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        # Обновляем логин, если он задан
        if new_username:
            user.username = new_username

        # Если хотя бы одно поле пароля заполнено, оба должны быть заполнены и совпадать
        if new_password or confirm_password:
            if new_password and confirm_password and new_password == confirm_password:
                user.set_password(new_password)
                update_session_auth_hash(request, user)  # чтобы не разлогинило
            else:
                error = "Пароли не совпадают или одно из полей пустое."
                return render(request, 'accounts/profile.html', {'user': user, 'error': error})
        user.save()
        return redirect('profile')
    return render(request, 'accounts/profile.html', {'user': user, 'error': error})



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
