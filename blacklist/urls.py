from django.urls import path
from .views import black_list, add_to_blacklist, success_page
urlpatterns = [
    path('black_list/', black_list, name = 'black_list'),
    path('add_to_blacklist/', add_to_blacklist, name = 'add_to_blacklist'),
    path('success/', success_page, name = 'success_page'),
]