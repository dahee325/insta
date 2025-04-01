from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .models import User
from django.contrib.auth.decorators import login_required

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

@login_required
def logout(request):
    auth_logout(request)
    return redirect('posts:index')


def profile(request, username):
    user_profile = User.objects.get(username=username)
    posts = user_profile.post_set.all().order_by('-created_at')

    context = {
        'user_profile': user_profile,
        'posts': posts,
    }
    return render(request, 'profile.html', context)


@login_required
def follow(request, username):
    me = request.user # 로그인한 사람
    you = User.objects.get(username=username) # 들어와있는 페이지의 사용자

    if me == you:
        return redirect('accounts:profile', username)

    # if you in me.followings.all():
    if me in you.followers.all():
        you.followers.remove(me)
        # 너의 팔로워 목록에서 나를 지워줘
        # me.followings.remove(you)
        # 나의 팔로잉 목록에서 너를 지워줘
    
    else:
        you.followers.add(me)
        # 너의 팔로워목록에 나를 추가해줘
        # me.followings.add(you)
        # 내 팔로잉 목록에 너를 추가해줘

    return redirect('accounts:profile', username)