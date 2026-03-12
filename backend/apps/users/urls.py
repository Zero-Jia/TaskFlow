from django.urls import path
from .views import health_check, register_user

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('users/register/', register_user, name='register_user'),
]