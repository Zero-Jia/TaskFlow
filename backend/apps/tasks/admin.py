from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'project',
        'status',
        'priority',
        'assignee',
        'creator',
        'due_date',
        'created_at',
    )
    list_filter = ('status', 'priority', 'project')
    search_fields = ('title', 'project__name', 'creator__username', 'assignee__username')