from django.urls import path
from django.contrib.auth.views import LoginView
from .views import profile, update_user_info

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('update_user_info/', update_user_info, name='update_user_info'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
]
