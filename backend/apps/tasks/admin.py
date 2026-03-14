from django.contrib import admin
from .models import Task, Comment, TaskAttachment


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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'task',
        'author',
        'created_at',
    )
    search_fields = (
        'task__title',
        'author__username',
        'content',
    )


@admin.register(TaskAttachment)
class TaskAttachmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'task',
        'file_name',
        'uploaded_by',
        'uploaded_at',
    )
    search_fields = (
        'task__title',
        'file_name',
        'uploaded_by__username',
    )