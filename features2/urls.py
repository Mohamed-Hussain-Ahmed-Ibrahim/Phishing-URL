from .views import features2, my_view2
from django.urls import path

urlpatterns = [
    path('features2/', features2, name = 'features2'),
    path('my_view2/', my_view2, name = 'my_view2'),
]