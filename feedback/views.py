from django.db import IntegrityError
from django.core.exceptions import ValidationError

from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.db import IntegrityError
from .forms import FeedbackForm
from .models import Feedback

# Create your views here.
def feedback(request):
    
    return render(request,'feedback.html')

from django.shortcuts import render
from .models import Feedback


def feedback_view(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        rate = request.POST['rate']
        Feedback.objects.create(subject=subject, rate=rate)
        return render(request, 'thanks.html')
    return render(request, 'feedback.html')




def feedback_success_view(request):
    return render(request, 'feedback_success.html')
