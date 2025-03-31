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
- `pip freeze >> requirements.txt` => `requirements.txt`폴더 생성
- 내가 설치한 라이브러리를 알려줌
- 새로운 라이브러리를 설치하면 위의 코드를 한번 더 해줘야함