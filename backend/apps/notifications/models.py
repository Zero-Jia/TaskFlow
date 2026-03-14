from django.conf import settings
from django.db import models


class Notification(models.Model):
    TYPE_CHOICES = (
        ('task_assigned', '任务指派'),
        ('task_comment', '任务评论'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='接收用户'
    )
    type = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES,
        verbose_name='通知类型'
    )
    content = models.CharField(
        max_length=255,
        verbose_name='通知内容'
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name='是否已读'
    )
    related_task_id = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='关联任务ID'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )

    class Meta:
        db_table = 'notification'
        verbose_name = '通知'
        verbose_name_plural = '通知'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.type}'