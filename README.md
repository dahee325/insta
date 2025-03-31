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
- `posts/templates/_card.html` \
=> 게시물을 작성한 유저 출력
=> 유저가 설정한 profile 사진 출력 (width="30px"로 크기 조정)
```html
<div class="card my-3" style="width: 18rem;">
    <div class="card-header">
        <img class="rounded-circle" src="{{post.user.profile_image.url}}" alt="" width="30px">
        <a href="">{{post.user.username}}</a>
    </div>
    ...
  </div>
```