from django.conf import settings
from django.db import models
from apps.projects.models import Project


class Task(models.Model):
    STATUS_CHOICES = (
        ('todo', '待处理'),
        ('in_progress', '进行中'),
        ('done', '已完成'),
        ('overdue', '已逾期'),
    )

    PRIORITY_CHOICES = (
        ('low', '低'),
        ('medium', '中'),
        ('high', '高'),
        ('urgent', '紧急'),
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='所属项目'
    )
    title = models.CharField(max_length=200, verbose_name='任务标题')
    description = models.TextField(blank=True, default='', verbose_name='任务描述')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='todo',
        verbose_name='任务状态'
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium',
        verbose_name='优先级'
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
        verbose_name='负责人'
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_tasks',
        verbose_name='创建人'
    )
    due_date = models.DateTimeField(null=True, blank=True, verbose_name='截止时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'task'
        verbose_name = '任务'
        verbose_name_plural = '任务'
        ordering = ['-created_at']

    def __str__(self):
        return self.title