from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# 让 Django Admin 能管理你的自定义用户模型。
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ('扩展信息', {'fields': ('avatar', 'bio', 'created_at')}),
    )
    readonly_fields = ('created_at',)
