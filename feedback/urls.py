from django.urls import path
from .views import feedback, feedback_view, feedback_success_view
urlpatterns = [
    path('feedback/', feedback, name = 'feedback'),
    path('feedback_view/', feedback_view, name = 'feedback_view'),
    path('feedback/success/', feedback_success_view, name='feedback_success'),
]