from .views import features3, my_view3
from django.urls import path

urlpatterns = [
    path('features3/', features3, name = 'features3'),
    path('my_view3/', my_view3, name = 'my_view3'),
]