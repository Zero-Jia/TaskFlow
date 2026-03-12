from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='邮箱')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='头像')
    bio = models.TextField(blank=True, default='', verbose_name='个人简介')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.username