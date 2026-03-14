from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'type',
        'content',
        'is_read',
        'related_task_id',
        'created_at',
    )
    list_filter = ('type', 'is_read')
    search_fields = ('user__username', 'content')