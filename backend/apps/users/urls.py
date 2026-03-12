from django.urls import path
from .views import health_check, register_user, login_user, user_profile

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('users/register/', register_user, name='register_user'),
    path('users/login/', login_user, name='login_user'),
    path('users/profile/', user_profile, name='user_profile'),
]