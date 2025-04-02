# 0. Setting
- `python -m venv venv`
- `source venv/Scripts/activate`
- `pip install django`
- `.gitignore` 설정


# 1. project 설치
- `django-admin startproject insta .`
- `django-admin startapp posts`
- `insta/settings.py` 에 `posts`앱 등록

# 2. 공통 base.html 생성
- `templates/base.html` 폴더랑 파일 생성
- `insta/settings.py` : `templates` 폴더 연결
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        '...
    },
]
```
- `templates/base.html` : bootstrap `<link>`랑 `<script>` 넣기

# 3. Post
## 3-1. modeling
- `posts/models.py` : [ImageField](https://docs.djangoproject.com/en/5.1/ref/forms/fields/#imagefield))
```python
class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='image')
```
## 3-2. Migration
- `python manage.py makemigrations` => Pillow(이미지 처리를 위한 라이브러리)를 설치하라고 에러가 남
- `pip install pillow`
- `python manage.py makemigrations`
- `python manage.py migrate`

## 3-3. admin 계정 만들기
- `posts/admin.py` : admin에 Post 모델 등록
```python
from django.contrib import admin
from .models import Post

# Register your models here.
admin.site.register(Post)
```
- `python manage.py createsuperuser`
- `python manage.py runserver` \
=> 만든 계정으로 로그인한 후 Posts에 게시글을 사진과 함께 등록하면 `image`폴더 생성\
=> 폴더 안에 등록한 사진 저장됨
- 생성된 `image`폴더는 코드가 아니라 임시 데이터일 뿐이므로 `.gitignore`에 `image`폴더 추가
- `insta/settings.py`파일의 마지막 줄에 `image/`추가

## 3-4. requirement.txt
- `pip freeze >> requirements.txt` => `requirements.txt`폴더 생성\
=> 현재 상태를 추가
- `pip freeze > requirements.txt`를 할 경우 현재 상태를 덮어씌움
- 내가 설치한 라이브러리를 알려줌
- 새로운 라이브러리를 설치하면 위의 코드를 한번 더 해줘야함

## 3-5. Read
- `insta/urls.py`
```python
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls'))
]
```
- `posts`폴더 안에 `urls.py`생성
```python
from django.urls import path
from m import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),
]
```
- `posts/views.py`
```python
from django.shortcuts import render
from .models import Post

def index(request):
    posts = Post.objects.all()

    context = {
        'posts': posts,
    }
    return render(request, 'index.html', context)
```
- `posts/templates/index.html`폴더랑 파일 생성
```html
{% extends 'base.html' %}

{% block body %}
    {% for post in posts%}
        <p>{{post.content}}</p>
        <p>{{post.image}}</p>
    {% endfor %}
{% endblock %}
```
## 3-6. Read 기능 업데이트
- `insta/settings.py` : 마지막에 추가
```python
# 업로드한 사진을 저장한 위치 (실제 폴더 경로)
MEDIA_ROOT = BASE_DIR / 'media'
# 미디어 경로를 처리할 URL, 
MEDIA_URL = '/media/'
```
- `insta/urls.py`
```python
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # concatenation
# static : 어떤 경로로 들어왔을 때, 어떤 경로로 가주세요 (경로/실제 파일의 위치)
# path('/image/cat.jpg', 'c/Desktop/damf2/insta/image/cat.jpg') => 이미지가 추가될 때마다 생성됨
```
- `posts/templates/index.html`
```html
        <p>{{post.image.url}}</p>
```
=> 위의 코드를 추가하면 페이지를 새로고침 했을 때 `/media/image/cat.jpg`파일의 경로가 출력되고 이 주소로 들어가면 해당하는 사진이 뜸
```html
        <img src="{{post.image.url}}" alt="">
```
=> 위의 코드를 추가하면 사진이 뜸

### Card
- `posts/templates/_card.html` 파일 생성 -> [card](https://getbootstrap.com/docs/5.3/components/card/) 그대로 복붙\
=> `style="width: 18rem;"` : 카드를 일정한 크기로 설정
```html
<div class="card" style="width: 18rem;">
  <img src="..." class="card-img-top" alt="...">
  <div class="card-body">
    <h5 class="card-title">Card title</h5>
    <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
    <a href="#" class="btn btn-primary">Go somewhere</a>
  </div>
</div>
```
- `posts/templates/index.html`\
=> `include` : 작은 모듈 단위의 html을 불러오는 명령어
```html
{% extends 'base.html' %}

{% block body %}
    {% for post in posts %}
        {% include '_card.html' %}
    {% endfor %}
{% endblock %}
```
- `posts/templates/_card.html` : 코드 수정
```html
<div class="card my-3" style="width: 18rem;">
    <div class="card-header">
        <p>username</p>
    </div>
    <img src="{{post.image.url}}" class="" alt="...">
    <div class="card-body">
      <!-- <h5 class="card-title">Card title</h5> -->
      <p class="card-text">{{post.content}}</p>
      <p class="card-text">{{post.created_at}}</p>
      <!-- <a href="#" class="btn btn-primary">Go somewhere</a> -->
    </div>
  </div>
```
- `templates/base.html`
```html
<body>
    <div class="container">
        {% block body %}
        {% endblock %}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
</body>
```

### Navbar
- `templates/_nav.html`파일 생성 -> [nav-bar](https://getbootstrap.com/docs/5.3/components/navbar/)
```html
<nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
        <a class="navbar-brand" href="#">Navbar</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div class="navbar-nav">
            <a class="nav-link active" aria-current="page" href="#">Home</a>
        <a class="nav-link" href="#">Features</a>
        <a class="nav-link" href="#">Pricing</a>
        <a class="nav-link disabled" aria-disabled="true">Disabled</a>
      </div>
    </div>
  </div>
</nav>
```
- `templates/base.html` : `_nav.html`연결
```html
<body>
    {% include '_nav.html'%} 
    <div class="container">
        {% block body %}
        {% endblock %}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
</body>
```
- `templates/_nav.html` : 코드 수정
```html
<nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
        <a class="navbar-brand" href="{% url 'posts:index' %}">Insta</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
          <div class="navbar-nav">
              <a class="nav-link" href="{% url 'posts:create' %}">Create</a>
          <a class="nav-link" href="#">Signup</a>
          <a class="nav-link" href="#">Login</a>
        </div>
      </div>
    </div>
  </nav>
```
## 3-7. Create
- `posts/urls.py`
```python
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
]
```
- `posts/views.py`
```python
def create(request):
    if request.method == 'POST':
        pass
    else:
        pass
```
- `posts/forms.py`파일 생성
```python
from django.forms import ModelForm
from .models import Post

class PostForm(ModelForm):
    class Meta():
        model = Post
        fields = '__all__'
```
- `post/views.py`
```python
from .forms import PostForm

def create(request):
    if request.method == 'POST':
        pass
    else:
        form = PostForm()

    context = {
        'form': form,
    }
    return render(request, 'create.html', context)
```
- `posts/templates/create.html`파일 생성
```html
{% block body%}
<form action="" method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    {{form}}
    <input type="submit">
</form>
{% endblock %}
```
=> `enctype` : 인코딩 타입, 파일을 업로드 할 때 사용해야하는 설정
- `posts/views.py` : if문 채우기
```python
from django.shortcuts import render, redirect

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
```
### [bootstrap5](https://pypi.org/project/django-bootstrap5/)
- `pip install django-bootstrap5`
- `insta/settings.py`에 `django_bootstrap5`등록
```python
INSTALLED_APPS = [
    ...
    'posts',
    'django_bootstrap5',
]
```
- `posts/templates/create.html`
```html
{% extends 'base.html' %}
{% load django_bootstrap5 %}

{% block body%}
<form action="" method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    {% bootstrap_form form %}
    <input type="submit" class="btn btn-primary">
</form>
{% endblock %}
```
### [resized](https://pypi.org/project/django-resized/)
- `posts/templates/_cards.html`에서 `style="width: 18rem;"`로 카드 크기를 설정해서 사진이 일정하게 보이지만 사진을 저장할 때 일정한 크기로 저장하는 것이 더 좋은 방법
- `pip install django-resized`
- `posts/models.py`
```python
from django.db import models
from django_resized import ResizedImageField

# Create your models here.
class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # image = models.ImageField(upload_to='image')
    image = ResizedImageField(
        size=[500, 500],
        crop=['middel', 'center'],
        upload_to='image/%Y/%m', 
        # 이미지 이름이 같은 파일은 다른 이름으로 저장됨
        # => /%Y/%m 연도를 기준으로 폴더을 만들고 그 안에 달을 기준으로 폴더를 더 만듦
    )
```

# 4. Account
## 4-1. makeproject
- `pip install startapp accounts`
- `insta/settings.py`에 `accounts`앱 등록
```python
INSTALLED_APPS = [
    ...
    'posts',
    'django_bootstrap5',
    'accounts',
]
```

## 4-2. modeling
- `accounts/models.py`
```python
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField

# Create your models here.
class User(AbstractUser):
    profile_image = ResizedImageField(
        size=[500, 500],
        crop=['middel', 'center'],
        upload_to='profile'
    )
```
- `insta/settings.py` : 새로운 User를 만들었으니 내가 만든걸 써달라고 말하기
```python
AUTH_USER_MODEL = 'accounts.User' # 마지막에 추가
```
- `posts/models.py`
```python
from django.conf import settings

# Create your models here.
class Post(models.Model):
    ...
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
```

## 4-3. Migration
- `python manage.py makemigrations`하면 에러가 생김 -> 기존 데이터에 User를 추가하면 기존에 있던 데이터의 USer에는 무엇을 넣어야돼? (디폴드값을 주거나 수동으로 models.py를 수정하거나 결정)
- `posts`와 `accounts`의 migration한 파일(`0001_initial.py`)을 지우고 `db.sqlite3`도 지우고 다시 migration실행
- `python manage.py makemigrations`
- `python manage.py migrate`

## 4-4. Signup
- `insta/urls.py`
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls')),
    path('accounts/', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
- `accounts/urls.py` 파일 생성
```python
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
]
```
- `accounts/views.py`
```python
from django.shortcuts import render

# Create your views here.
def signup(request):
    if request.method == 'POST':
        pass
    else:
        pass
```
- `accounts/forms.py`파일 생성
```python
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta():
        model = User
        fields = ('username', 'profile_image', )
```
- `accounts/views.py`
```python
from django.shortcuts import render
from .forms import CustomUserCreationForm

# Create your views here.
def signup(request):
    if request.method == 'POST':
        pass
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'signup.html', context)
```
- `accounts/templates/signup.html` 폴더랑 파일 생성
```html
{% extends 'base.html' %}
{% load django_bootstrap5 %}

{% block body %}
    <form action="" method="POST" enctype="multipart/form-data">
        {% csrf_token %}
        {% bootstrap_form form %}
        <input type="submit">
    </form>
{% endblock %}
```
- `accounts/views.py` : if문 채우기
```python
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts:index')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'signup.html', context)
```

## 4-5. Login
- `accounts/urls.py`
```python
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
]
```
- `accounts/views.py`
```python
def login(request):
    if request.method == 'POST':
        pass
    else:
        pass
```
- `accounts/forms.py`
```python
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    pass
```
- `accounts/views.py`
```python
from .forms import CustomUserCreationForm, CustomAuthenticationForm

def login(request):
    if request.method == 'POST':
        pass
    else:
        form = CustomAuthenticationForm()

    context = {
        'form': form,
    }
    return render(request, 'login.html', context)
```
- `accounts/templates/login.html`파일 생성
```html
{% extends 'base.html' %}
{% load django_bootstrap5 %}
{% block body %}
    <form action="" method="POST">
        {% csrf_token %}
        {% bootstrap_form form %}
        <input type="submit" class="btn btn-primary">
    </form>
{% endblock %}
```
- `accounts/views.py`
```python
from django.contrib.auth import login as auth_login

def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user() # 내가 로그인하려고하는 유저의 정보(id, password)를 빼오기
            auth_login(request, user) # 빼온 정보(user)를 바탕으로 session을 발급받아 cookies(request)에 넣고 로그인
            return redirect('posts:index')

    else:
        form = CustomAuthenticationForm()

    context = {
        'form': form,
    }
    return render(request, 'login.html', context)
```

## 4-6. Logout
- `accounts/urls.py`
```python
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
```
- `accounts/views.py`
```python
from django.contrib.auth import logout as auth_logout

def logout(request):
    auth_logout(request)
    return redirect('posts:index')
```

### navbar 링크 연결
- `templates/_nav.html`
```html
<nav class="navbar navbar-expand-lg bg-body-tertiary">
    ...
      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div class="navbar-nav">
            {% if user.is_authenticated %}
            <a class="nav-link" href="{% url 'posts:create' %}">Create</a>
            <a class="nav-link" href="{% url 'accounts:logout' %}">Logout</a>
            <a class="nav-link disabled" href="">{{user}}</a>
            {% else %}
            <a class="nav-link" href="{% url 'accounts:signup' %}">Signup</a>
            <a class="nav-link" href="{% url 'accounts:login' %}">Login</a>
            {% endif %}
        </div>
      </div>
    </div>
  </nav>
```

# 5. Post
## 5-1. Create
- `posts/forms.py`
```python
class PostForm(ModelForm):
    class Meta():
        model = Post
        # fields = '__all__'
        fields = ('content', 'image', )
```
- `posts/views.py`\
=> 로그인한 사람만 create함수를 실행할 수 있게 설정
=> 게시물을 누가 작성했는지 user정보 추가
```python
from django.contrib.auth.decorators import login_required

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
```

## 5-2. card 업데이트
- `posts/templates/_card.html` \
=> 게시물을 작성한 유저 출력
=> 유저가 설정한 profile 사진 출력 (width="30px"로 크기 조정)
=> `timesince` : 장고가 미리 구현해놓은 작성한 시간이 출력되는 것이 아니라 몇 초/분/시간 전에 작성된 게시글인지 출력
```html
<div class="card my-3" style="width: 18rem;">
    <div class="card-header">
        <img class="rounded-circle" src="{{post.user.profile_image.url}}" alt="" width="30px">
        <a href="">{{post.user.username}}</a>
    </div>
    ...
  </div>
```


### bootstrap [Icons](https://icons.getbootstrap.com/)
- `templates/base.html` : <link> 복붙
```html

```
- `templates/_nav.html`
```html
<nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <a class="navbar-brand" href="{% url 'posts:index' %}">
        <i class="bi bi-instagram"></i>
        Insta
      </a>
      ...
    </div>
  </nav>
```

### 게시물을 작게 만들기
- `posts/templates/index.html`
```html
{% block body %}
    <div class="row">
        {% for post in posts %}
            {% include '_card.html' %}
        {% endfor %}
    </div>
{% endblock %}
```
- `posts/templates/_card.html`
```html
<!-- <div class="card my-3 col-12 col-md-6 col-xl-4"> -->
<!--col-xl-4 : 게시물의 크기 설정-->
<div class="card my-3 col-12 offset-md-2 col-xl-4" style="width: 18rem;">
<!--offset-md-2 : 앞에 2칸을 비워주세요-> 마지막은 자동으로 4칸-->
    ...
</div>
```

# 6. Comment
## 6-1. modeling 
- `posts/models.py`
```python
class Comment(models.Model):
    content = models.CharFiedl(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
```

## 6-2. Migration
- `python manage.py makemigrations`
- `python manage.py migrate`

## 6-3. Create
- `posts/urls.py`
```python
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),

    path('<int:post_id>/comments/create/', views.comment_create, name='comment_create'),
]
```
- `posts/forms.py`
```python
from .models import Post, Comment

class CommentForm(ModelForm):
    class Meta():
        model = Comment
        fields = ('content', )
```
- `posts/views.py` : `index`함수 수정
```python
from .forms import PostForm, CommentForm

def index(request):
    posts = Post.objects.all()
    form = CommentForm
    context = {
        'posts': posts,
        'form': form,
    }
    return render(request, 'index.html', context)
```
- `posts/templates/index.html` : `{% include '_card.html' %}`부분 때문에 `_card.html`에 댓글폼 생성

- `posts/templates/_card.html` : **bootstrap** 사용\
=> `<div class="row">`은 댓글 form을 한 줄로 만들어줌\
=> `show_label=False` : 라벨을 출력하지 않음\
=> `wrapper_class=''` : `mb-3`이 디폴트, 빈값으로 둬서 마진을 뺌
=> 댓글폼 만들고 `comment_create`로 링크도 연결
```html
{% load django_bootstrap5 %}
<div class="card my-3 p-0 col-12 offset-md-4 col-xl-4">

    ...
    <div class="card-footer">
      <form action="{% url 'posts:comment_create' post.id %}" method="POST">
        {% csrf_token %}
        <div class="row">
          <div class="col-9"> <!--12칸 중 9칸 차지-->
            {% bootstrap_form form show_label=False wrapper_class='' %}
            <!-- show_label=False : 라벨출력X -->
            <!-- wrapper_class='' : mb-3이 디폴트, 빈값으로 둬서 마진을 뺌-->
          </div>
          <div class="col-2"> <!--12칸 중 2칸 차지-->
            <input type="submit" class="btn btn-primary">
          </div>
        </div>
      </form>
    </div>
  </div>
```
- `posts/views.py`
```python
@login_required # 로그인 한 사람만 comment_create 실행
def comment_create(request, post_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post_id = post_id
        comment.save()
        return redirect('posts:index')
```
=> 로그아웃해도 comment창이 보임 => 로그인했을 때만 보여지게 설정
```html
<div class="card my-3 p-0 col-12 offset-md-4 col-xl-4">

    ...
    <div class="card-footer">
      {% if user.is_authenticated %}
      <form action="{% url 'posts:comment_create' post.id %}" method="POST">
        {% csrf_token %}
        <div class="row">
          <div class="col-9"> <!--12칸 중 9칸 차지-->
            {% bootstrap_form form show_label=False wrapper_class='' %}
            <!-- show_label=False : 라벨출력X -->
            <!-- wrapper_class='' : mb-3이 디폴트, 빈값으로 둬서 마진을 뺌-->
          </div>
          <div class="col-2"> <!--12칸 중 2칸 차지-->
            <input type="submit" class="btn btn-primary">
          </div>
        </div>
      </form>
      {% endif %}
    </div>
  </div>
```

## 6-4. Read
- `posts/templates/_card.html`
```html
<div class="card my-3 p-0 col-12 offset-md-4 col-xl-4">

    ...
    <div class="card-footer">
      {% if user.is_authenticated %}
      <form action="{% url 'posts:comment_create' post.id %}" method="POST">
        {% csrf_token %}
        ...
      </form>
      {% endif %}
      <div class="mt-2">
        {% for comment in post.comment_set.all %}
          <li>{{comment.user}} : {{comment.content}}</li>
        {% endfor %}
      </div>
    </div>
  </div>
```


# 7. M : N 관계 -> Like
- M:N 관계에서는 중간테이블이 꼭 필요함\
=> 병원에서 의사와 환자의 경우 예약테이블이 꼭 필요함\
=> 의사와 예약은 1:N의 관계, 환자와 예약은 1:N의 관게
- 인스타그램 게시물에 좋아요를 다는 경우\
=> 게시물(Post)과 사용자(user) 사이에 좋아요(like)테이블 필요
=> like테이블은 user_id와 post_id를 갖고있음

## 7-1. modeling
- `posts/models.py` : `Post`함수에 `like_users`추가
```python
class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # image = models.ImageField(upload_to='image')
    image = ResizedImageField(
        size=[500, 500],
        crop=['middle', 'center'],
        upload_to='image/%Y/%m', 
        # 이미지 이름이 같은 파일은 다른 이름으로 저장됨
        # => /%Y/%m 연도를 기준으로 폴더을 만들고 그 안에 달을 기준으로 폴더를 더 만듦
    )
    # 작성자 저장
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    # 게시물에 좋아요를 단 사람들 저장
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='like_posts', # post_set이 user에 의해 만들어졌는데 like_users가 또 만들려고 시도해서 migration을 하면 에러가 생김
        # => related_name을 사용해서 like_users에서 생성되는 post_set의 이름을 지정
    )
```

## 7-2. Migration
- `python manage.py makemigrations`
- `python manage.py migrate`

## 7-3. 좋아요 버튼 생성
- `posts/templates/_card.html`
- bootstrap icon 사용해서 하트 버튼 생성
```html
<div class="card my-3 p-0 col-12 offset-md-4 col-xl-4">

    ...
    <img src="{{post.image.url}}" class="" alt="...">
    <div class="card-body">
      <a href="{% url 'posts:like' post.id %}">
        <i class="bi bi-heart"></i>
      </a>
      ...
    </div>
    ...
</div>
```
- `posts/url.py`
```python
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),

    path('<int:post_id>/comments/create/', views.comment_create, name='comment_create'),
    path('<int:post_id>/like/', views.like, name='like'),
]
```
- `post/views.py`
```python
def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)

    # if post in user.like_posts.all():
    # post가 user가 누른 게시물 목록에 있나요?
    if user in post.like_users.all():
    # user가 post에 좋아요를 누른 사람의 목록에 있나요?

        # 좋아요 취소
        user.like_posts.remove(post)
        # post가 user가 좋아요를 누른 게시물의 목록에 있다면 post를 목록에서 제거
        post.like_users.remove(user)
        # user가 post에 좋아요를 누른 사용자의 목록에 있다면 user를 목록에서 제거
    else:
        # user.like_posts.add(post)
        # post가 목록에 없으면 user가 누른 게시물 목록에 post를 추가
        post.like_users.add(user)
        # user가 목록에 없으면 좋아요를 누른 사람들의 목록에 user를 추가

    return redirect('posts:index')
```
- `posts/templates/_cared.html`
```html
<div class="card my-3 p-0 col-12 offset-md-4 col-xl-4">

    ...
    <img src="{{post.image.url}}" class="" alt="...">
    <div class="card-body">
      <a href="{% url 'posts:like' post.id %}">
        <i class="bi bi-heart"></i>
      </a>
      <span>{{post.like_users.all|length}}명이 좋아합니다.</span>
      ...
    </div>
    ...
</div>
```
- 좋아요 버튼(하트모양) 색 바꾸기
=> `class="text-reset"` : 링크를 눌렀을 때 흑백처리
```html
<div class="card my-3 p-0 col-12 offset-md-4 col-xl-4">

    ...
    <img src="{{post.image.url}}" class="" alt="...">
    <div class="card-body">
      <a href="{% url 'posts:like' post.id %}" class="text-reset text-decoration-none">
        <i class="bi bi-heart"></i>
      </a>
      <span>{{post.like_users.all|length}}명이 좋아합니다.</span>
      ...
    </div>
    ...
</div>
```
- 좋아요 버튼을 눌렀을 때 하트 채우기
```html
<div class="card my-3 p-0 col-12 offset-md-4 col-xl-4">

    ...
    <img src="{{post.image.url}}" class="" alt="...">
    <div class="card-body">
      <a href="{% url 'posts:like' post.id %}" class="text-reset text-decoration-none">
        {% if user in post.like_users.all %}
          <i class="bi bi-heart-fill" style="color: red;"></i>
        {% else %}
          <i class="bi bi-heart"></i>
        {% endif %}
      </a>
      <span>{{post.like_users.all|length}}명이 좋아합니다.</span>
      ...
    </div>
    ...
</div>
```


### `posts/forms.py`
exclude = ('user', 'like_users', )

# 8. Profile
- `posts/templates/_card.html` : username을 누르면 profile 페이지로 이동
```html
<div class="card my-3 p-0 col-12 offset-md-4 col-xl-4">
    <div class="card-header">
        <img class="rounded-circle" src="{{post.user.profile_image.url}}" alt="" width="30px">
        <a href="{% url 'accounts:profile' post.user.username %}">{{post.user.username}}</a>
    </div>
    ...
  </div>
```
- `accounts/urls.py` : `profile`경로 생성
```python
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<username>/', views.profile, name='profile'),
]
```
- `accounts/views.py`
```python
from .models import User

def profile(request, usernmae):
    user_profile = User.objects.get(username=username)

    context = {
        'user_profile': user_profile,
    }
    return render(request, 'profile.html', context)
```
- `accounts/templates/profile.html` 파일 생성
```html
{% extends 'base.html' %}

{% block body %}
    <div class="row my-3">
        <!--프로필 사진-->
        <div class="col-3">
            <img src="{{user_profile.profile_image.url}}" alt="" class="img-fluid rounded-circle">
        </div>
        <div class="col-9">
            <!--이름과 팔로우 버튼-->
            <div class="row">
                <div class="col-3">{{user_profile.username}}</div>
                <div class="col-9">팔로우</div>
            </div>
            <!--게시물, 팔로워, 팔로우 수-->
            <div class="row">
                <div class="col-4">게시물 :</div>
                <div class="col-4">팔로워 :</div>
                <div class="col-4">팔로우 : </div>
            </div>
        </div>
    </div>
    <div class="row">
        {% for post in user_profile.post_set.all %}
            <div class="col-4">
                <img src="{{post.image.url}}" alt="" class="img-fluid">
            </div>
        {% endfor %}
    </div>
{% endblock %}
```

# 9. Follow
- `accounts/models.py` : following 기능 모델링
```python
class User(AbstractUser):
    profile_image = ResizedImageField(
        size=[500, 500],
        crop=['middle', 'center'],
        upload_to='profile'
    )

    followings = models.ManyToManyField('self', related_name='followers', symmetrical=False)
    # 'self' : user와 user를 서로 m:n으로 연결
    # 'related_name=''' : 반대쪽에서 뭐라고 부를지 지정
    # symmetrical=False : 비대칭 / 1->2팔로우하는 것과 2->1팔로우 하는 것이 다르니까 False로 지정
    # followings : 내가 팔로우하는 사람들
    # followers : 나를 팔로우하는 사람들
```
- `accounts/templates/profile.html`
```html

```
- `accounts/urls.py`
```python
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<username>/', views.profile, name='profile'),
    path('<username>/follow/', views.follow, name='follow'),
]
```
- `accounts/viewws.py`
```python
def follow(request, username):
    me = request.user # 로그인한 사람
    you = User.objects.get(username=username) # 들어와있는 페이지의 사용자

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
```
- `accounts/templates/profile.html`
```html
{% block body %}
    <div class="row my-3">
        ...
        <div class="col-9">
            ...
            <!--게시물, 팔로워, 팔로우 수-->
            <div class="row">
                <div class="col-4">게시물 : {{user_profile.post_set.all|length}}</div>
                <div class="col-4">팔로워 : {{user_profile.followers.all|length}}</div>
                <div class="col-4">팔로우 : {{user_profile.followings.all|length}}</div>
            </div>
        </div>
    </div>
    ...
{% endblock %}
```
- 자신의 프로필 페이지에서는 follow버튼 안보이게 하기
- `accounts/templates/profile.html`
```html
{% extends 'base.html' %}

{% block body %}
    <div class="row my-3">
        ...
        <div class="col-9">
            <!--이름과 팔로우 버튼-->
            <div class="row">
                <div class="col-3">{{user_profile.username}}</div>
                {% if user != user_profile %}
                <!--로그인한 사람과 보고있는 프로필의 사용자가 다르면 버튼을 보여줌-->
                <div class="col-9">
                    <a href="{% url 'accounts:follow' user_profile.username %}" class="btn btn-primary">팔로우</a>
                </div>
                {% endif %}
            </div>
            ...
        </div>
    </div>
    ...
{% endblock %}
```
- `accounts/views.py`
```python
from django.contrib.auth.decorators import login_required

@login_required
def follow(request, username):
    ...
    if me == you:
        return redirect('accounts:profile', username)
    ...
```
- `accounts/views.py`의 `Logout`함수와 `posts/views.py`의 `Like`함수에도 `@login_required` 붙여서 로그인했을 때만 실행 가능하게 설정
- `accounts/templates/profile.html` : 팔로우가 되어있으면 팔로우취소 버튼을 보여주고 팔로우가 안되어있으면 팔로우 버튼을 보여줌
```html
{% block body %}
    <div class="row my-3">
        ...
            <!--이름과 팔로우 버튼-->
            <div class="row">
                <div class="col-3">{{user_profile.username}}</div>
                {% if user != user_profile %}
                <!--로그인한 사람과 보고있는 프로필의 사용자가 다르면 버튼을 보여줌-->
                <div class="col-9">
                    {% if user in user_profile.followers.all %}
                        <a href="{% url 'accounts:follow' user_profile.username %}" class="btn btn-secondary">팔로우취소</a>
                    {% else %}
                        <a href="{% url 'accounts:follow' user_profile.username %}" class="btn btn-primary">팔로우</a>
                    {% endif %}
                </div>
                {% endif %}
            </div>
            ...
        </div>
    </div>
    ...
{% endblock %}
```

# 10. Feed
- 내가 팔로우한 사람들의 피드만 보이이게하는 페이지
- `templates/_nav.html`
```html
<nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      ...
      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div class="navbar-nav">
            {% if user.is_authenticated %}
            ...
            <a class="nav-link" href="{% url 'posts:feed' %}">feed</a>
            <a class="nav-link disabled" href="">{{user}}</a>
            {% else %}
            ...
            {% endif %}
        </div>
      </div>
    </div>
  </nav>
```
- `posts/urls.py`
```python
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),

    path('<int:post_id>/comments/create/', views.comment_create, name='comment_create'),
    path('<int:post_id>/like/', views.like, name='like'),
    path('feed/', views.feed, name='feed'),
]
```
- `posts/views.py`
```python
def feed(request):
    followings = request.user.followings.all()

    # 내가 팔로우하는 사람들의 게시물 목록
    posts = Post.objects.filter(user__in=followings)
    form = CommentForm()

    context = {
        'posts': posts,
        'form': form,
    }
    return render(request, 'index.html', context)
```

## 내가 추가한 기능
### navbar의 username을 누르면 로그인한 user의 profile페이지로 연결
- `templates/_nav.html`
```html
<a class="nav-link" href="{% url 'accounts:profile' user.username %}">{{user}}</a>
```

### index 게시글 최신순으로 바꾸기
- `posts.views.py`
```python
def index(request):
    posts = Post.objects.all()
    posts = Post.objects.order_by('-created_at') # 추가
    form = CommentForm
    context = {
        'posts': posts,
        'form': form,
    }
    return render(request, 'index.html', context)
```

### Comment 목록 수정
- 리스트가 아닌 a태그를 사용, username만 진하게 표시
- `posts/templates/_card.html`
```html
      <div class="mt-2">
        {% for comment in post.comment_set.all %}
          <a><strong>{{comment.user}}</strong> : {{comment.content}}</a>
        {% endfor %}
      </div>
```

### Read(1) - detail페이지 만들기
- `accounts/templates/profile.html` : a태그로 감싸서 detail로 링크 연결
```html
        {% for post in user_profile.post_set.all %}
            <div class="col-4">
                <a href="{% url 'posts:detail' post.id %}">
                    <img src="{{post.image.url}}" alt="" class="img-fluid">
                </a>
            </div>
        {% endfor %}
```
- `posts/urls.py`
```python
    path('<int:post_id>/', views.detail, name='detail'), # 추가
```
- `posts/views.py`
```python
def detail(request, post_id):
    post = Post.objects.get(id=post_id)
    form = CommentForm
    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'detail.html', context)
```
- `posts/templates/detail.html` 파일 생성
```html
{% extends 'base.html' %}
{% load django_bootstrap5 %}

{% block body %}
    <div class="row">
        <div class="card my-3 p-0 col-12 offset-md-4 col-xl-4">
            <div class="card-header">
                <img class="rounded-circle" src="{{post.user.profile_image.url}}" alt="" width="30px">
                <a href="{% url 'accounts:profile' post.user.username %}">{{post.user.username}}</a>
            </div>
            <img src="{{post.image.url}}" class="" alt="...">
            <div class="card-body">
                <a href="{% url 'posts:like' post.id %}" class="text-reset text-decoration-none">
                {% if user in post.like_users.all %}
                    <i class="bi bi-heart-fill" style="color: red;"></i>
                {% else %}
                    <i class="bi bi-heart"></i>
                {% endif %}
                </a>
                <span>{{post.like_users.all|length}}명이 좋아합니다.</span>
                <!-- <h5 class="card-title">Card title</h5> -->
                <p class="card-text">{{post.content}}</p>
                <p class="card-text">{{post.created_at|timesince}}</p>
                <!-- <a href="#" class="btn btn-primary">Go somewhere</a> -->
            </div>
            <div class="card-footer">
                {% if user.is_authenticated %}
                <form action="{% url 'posts:comment_create' post.id %}" method="POST">
                {% csrf_token %}
                <div class="row">
                    <div class="col-9"> <!--12칸 중 9칸 차지-->
                    {% bootstrap_form form show_label=False wrapper_class='' %}
                    <!-- show_label=False : 라벨출력X -->
                    <!-- wrapper_class='' : mb-3이 디폴트, 빈값으로 둬서 마진을 뺌-->
                    </div>
                    <div class="col-2"> <!--12칸 중 2칸 차지-->
                    <input type="submit" class="btn btn-primary">
                    </div>
                </div>
                </form>
                {% endif %}
                <div class="mt-2">
                {% for comment in post.comment_set.all %}
                    <a><strong>{{comment.user}}</strong> : {{comment.content}}</a>
                {% endfor %}
                </div>
            </div>
        </div>
    </div>
{% endblock %}
```

### Update, Delete
- `posts/templates/detail.html` : 게시물 작성 시간 아래에 버튼 만들기
```html
{% if user == post.user %}
<a class="btn btn-warning" href="{% url 'posts:update' post.id %}">수정</a>
<a class="btn btn-danger" href="{% url 'posts:delete' post.id %}">삭제</a>
{% endif %}
```
- `posts/urls.py`
```python
    path('<int:post_id>/update/', views.update, name='update'),
    path('<int:post_id>/delete/', views.delete, name='delete'),
```
- `posts/views.py`
```python
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
```
- `posts/templates/update.html`
```html
{% extends 'base.html' %}
{% load django_bootstrap5 %}

{% block body%}
<form action="" method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    {% bootstrap_form form %}
    <input type="submit" class="btn btn-warning" value="수정">
</form>
{% endblock %}
```

### detail 페이지의 게시글 최신순으로 바꾸기
1. 함수에 인자 지정해서 사용
- `accounts.views.py` : `profile`함수에 posts인자 추가
```python
def profile(request, username):
    user_profile = User.objects.get(username=username)
    posts = user_profile.post_set.all().order_by('-created_at') # 추가

    context = {
        'user_profile': user_profile,
        'posts': posts, # 추가
    }
    return render(request, 'profile.html', context)
```
- `accounts/templates/profile.html`
```html
<!--{% for post in user_profile.post_set.all %}을 밑처럼 수정-->
{% for post in posts %}
```

2. html에서 수정하기
- `accounts/templates/profile.html` : `dictsortreversed`함수를 사용하여 정렬
```html
{% for post in user_profile.post_set.all|dictsortreversed:'created_at' %}
```

# 11. JavaScript
- `posts/templates/index.html`
```html
{% block body %}
    ...
    <script>
        console.log('hello')
    </script>
{% endblock %}
```
=> 자바스크립트 쓸 준비 완료
- `posts/templates/_card.html` : 하트 icon의 `class`에 `like` 추가
-  `<a>`태그 지우기 => url이 아닌 자바스크립트로 보내기 위해서
```html
        {% if user in post.like_users.all %}
          <i class="bi like bi-heart-fill" style="color: red;"></i>
        {% else %}
          <i class="bi like bi-heart"></i>
        {% endif %}
```
- `posts/templates/index.html`
```html
    <script>
        let likeBtns = document.querySelectorAll('i.like')
        
        likeBtns.forEach(function(likeBtns){
            likeBtns.addEventListener('click', function(e){
                console.log(e.target)
            })
        })

    </script>
```
- `posts/templates/_card.html` : 하트를 눌렀을 때 몇번 게시물인지 출력하기
```html
        {% if user in post.like_users.all %}
          <i class="bi like bi-heart-fill" style="color: red;" data-post-id="{{post.id}}"></i>
        {% else %}
          <i class="bi like bi-heart" data-post-id="{{post.id}}"></i>
        {% endif %}
```
- `posts/templates/index.html`
```html
    <script>
        let likeBtns = document.querySelectorAll('i.like')
        
        // 장고 서버로 요청 보내기 -> 요청을 토대로 하트 결과를 바꿔줌
        let likeRequest = async (btn, postId) => {
            let likeURL = `/posts/${postId}/like-async` // 다른 url하나 더 만들기
            
            let res = fetch(likeURL)
        }

        likeBtns.forEach(function(likeBtn){
            likeBtn.addEventListener('click', function(e){
                const postId = e.target.dataset.postId // icon에서 게시물id를 data-post-id로 설정해서 dataset.postId로 접근
                
                likeRequest(likeBtn, postId)
            })
        })

    </script>
```
- `posts/urls.py`
```python
urlpatterns = [
    ...
    path('<int:id>/like-async/',views.like_async, name='like_async'),
]
```
- `posts/views.py`
```python
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
```
- `posts/templates/_card.html` : 좋아요 개수를 `<i>`태그 안의 `<span>`태그를 만들어 넣음
```html
        {% if user in post.like_users.all %}
          <i class="bi like bi-heart-fill" style="color: red;" data-post-id="{{post.id}}">
            <span>{{post.like_users.all|length}}</span>
          </i>
        {% else %}
          <i class="bi like bi-heart" data-post-id="{{post.id}}">
            <span>{{post.like_users.all|length}}v</span>
          </i>
        {% endif %}
      <span>명이 좋아합니다.</span>
```
- `posts/templates/index.html`
```html
    <script>
        let likeBtns = document.querySelectorAll('i.like')
        
        // 장고 서버로 요청 보내기 -> 요청을 토대로 하트 결과를 바꿔줌
        let likeRequest = async (btn, postId) => {
            let likeURL = `/posts/${postId}/like-async`
            
            let res = await fetch(likeURL)
            let result = await res.json()

            if (result.status) { // status가 true면 빨강색으로
                btn.style.color = 'red'
                btn.classList.remove('bi-heart')
                btn.classList.add('bi-heart-fill')
            } else {
                btn.style.color = 'black'
                btn.classList.remove('bi-heart-fill')
                btn.classList.add('bi-heart')
            }
            btn.querySelector('span').innerHTML = result.count // btn은 <i>를 의미
        }

        ...

    </script>
```
- `posts/templates/_card.html` : 하트 색이 바뀔 때 숫자가 같이 바뀜 => 검정색으로 변환
```html
        {% if user in post.like_users.all %}
          <i class="bi like bi-heart-fill" style="color: red;" data-post-id="{{post.id}}">
            <span style="color: black">{{post.like_users.all|length}}</span>
          </i>
        {% else %}
          <i class="bi like bi-heart" data-post-id="{{post.id}}">
            <span style="color: black">{{post.like_users.all|length}}v</span>
          </i>
        {% endif %}
      <span>명이 좋아합니다.</span>
```