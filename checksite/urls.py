from .views import check_site
from django.urls import path

urlpatterns = [
    path('check_site/', check_site, name = 'check_site'),
]