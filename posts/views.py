from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm

# Create your views here.
def index(request):
    posts = Post.objects.all()

    context = {
        'posts': posts,
    }
    return render(request, 'index.html', context)


def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES) # request.FILES : 사진이 들어있는 공간
        if form.is_valid():
            form.save()
            return redirect('posts:index')
    else:
        form = PostForm()

    context = {
        'form': form,
    }
    return render(request, 'create.html', context)