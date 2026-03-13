from django.conf import settings
from django.db import models
from apps.teams.models import Team


class Project(models.Model):
    STATUS_CHOICES = (
        ('active', '进行中'),
        ('completed', '已完成'),
        ('archived', '已归档'),
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='projects',
        verbose_name='所属团队'
    )
    name = models.CharField(max_length=100, verbose_name='项目名称')
    description = models.TextField(blank=True, default='', verbose_name='项目描述')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='项目状态'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_projects',
        verbose_name='创建人'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'project'
        verbose_name = '项目'
        verbose_name_plural = '项目'
        ordering = ['-created_at']

    def __str__(self):
        return self.name