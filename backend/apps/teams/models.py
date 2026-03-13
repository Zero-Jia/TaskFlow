# 定义模型
from django.conf import settings
from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name='团队名称')
    description = models.TextField(blank=True, default='', verbose_name='团队描述')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_teams',
        verbose_name='团队拥有者'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'team'
        verbose_name = '团队'
        verbose_name_plural = '团队'

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    ROLE_CHOICES = (
        ('owner', '拥有者'),
        ('admin', '管理员'),
        ('member', '普通成员'),
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='members',
        verbose_name='所属团队'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='team_memberships',
        verbose_name='团队成员'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='member',
        verbose_name='角色'
    )
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name='加入时间')

    class Meta:
        db_table = 'team_member'
        verbose_name = '团队成员'
        verbose_name_plural = '团队成员'
        unique_together = ('team', 'user')

    def __str__(self):
        return f'{self.user.username} - {self.team.name} ({self.role})'