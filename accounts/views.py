from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'signup.html', context)


def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user() # 내가 로그인하려고하는 유저의 정보(id, password)
            auth_login(request, user)
            return redirect('posts:index')

    else:
        form = CustomAuthenticationForm()

    context = {
        'form': form,
    }
    return render(request, 'login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('posts:index')