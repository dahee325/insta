from django.db import models
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField

# Create your models here.
class User(AbstractUser):
    profile_image = ResizedImageField(
        size=[500, 500],
        crop=['middle', 'center'],
        upload_to='profile'
    )

    followings = models.ManyToManyField('self', related_name='followers', symmetrical=False)
    # 'self' : user와 user를 서로 m:n으로 연결
    # 'related_name=''' : 반대쪽에서 뭐라고 부를지 지정
    # symetrical=False : 비대칭 / 1->2팔로우하는 것과 2->1팔로우 하는 것이 다르니까 False로 지정
    # followings : 내가 팔로우하는 사람들
    # followers : 나를 팔로우하는 사람들