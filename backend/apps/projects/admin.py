from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'team', 'status', 'created_by', 'created_at')
    list_filter = ('status', 'team')
    search_fields = ('name', 'team__name', 'created_by__username')
