from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.
def index(request):
    posts = Post.objects.all()
    posts = posts.order_by('-created_at')
    form = CommentForm
    context = {
        'posts': posts,
        'form': form,
    }
    return render(request, 'index.html', context)


def detail(request, post_id):
    post = Post.objects.get(id=post_id)
    form = CommentForm
    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'detail.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES) # request.FILES : 사진이 들어있는 공간
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:index')
    else:
        form = PostForm()

    context = {
        'form': form,
    }
    return render(request, 'create.html', context)

@login_required
def update(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:detail', post_id=post.id)
    else:
        form = PostForm(instance=post)

    context = {
        'form': form,
    }
    return render(request, 'update.html', context)

@login_required
def delete(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('accounts:profile', username=post.user.username)


@login_required
def comment_create(request, post_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post_id = post_id
        comment.save()
        return redirect('posts:index')

@login_required
def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)

    # if post in user.like_posts.all():
    if user in post.like_users.all():
        # 좋아요 취소
        user.like_posts.remove(post)
        post.like_users.remove(user)
    else:
        # user.like_posts.add(post)
        post.like_users.add(user)

    return redirect('posts:index')


def feed(request):
    followings = request.user.followings.all()

    # 내가 팔로우하는 사람들의 게시물 목록
    posts = Post.objects.filter(user__in=followings)
    posts = posts.order_by('-created_at')
    form = CommentForm()

    context = {
        'posts': posts,
        'form': form,
    }
    return render(request, 'index.html', context)


def like_async(request, id):
    user = request.user
    post = Post.objects.get(id=id)
    
    if user in post.like_users.all():
        post.like_users.remove(user)
        status = False # 좋아요 취소
    else:
        post.like_users.add(user)
        status = True # 좋아요 추가

    context = {
        'post_id': id, # 게시물 id
        'status': status, # 좋아요를 추가했는지 취소했는지 알려줌
        'count': len(post.like_users.all()) # 현재 시점의 게시물의 좋아요 개수
    } # 자바스크립트가 볼 수 있는 json으로 바꿔줘야함 => JsonResponse
    return JsonResponse(context) # => index.html의 res가 받음