from django.urls import path
from .views import register, Login, Logout




urlpatterns = [
    path('register/', register, name = 'register'),
    path('login/', Login, name = 'login'),
    path('logout/', Logout, name='logout'),
]