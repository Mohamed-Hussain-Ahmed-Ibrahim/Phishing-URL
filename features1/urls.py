from .views import features1, my_view1, store
from django.urls import path

urlpatterns = [
    path('features1/', features1, name = 'features1'),
    path('my_view1/', my_view1, name = 'my_view1'),
    path('store/', store, name='store'),
]