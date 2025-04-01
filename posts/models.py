from django.db import models
from django_resized import ResizedImageField
from django.conf import settings

# Create your models here.
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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )


class Comment(models.Model):
    content = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)