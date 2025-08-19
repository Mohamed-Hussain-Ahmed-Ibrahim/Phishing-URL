from django.shortcuts import render, redirect
from .models import BlacklistURL
from django.urls import reverse
from .models import BlacklistURL
# Create your views here.
def black_list(request):
    return render(request,'Blacklist.html')



def success_page(request):
    return render(request,'success_page.html')

def add_to_blacklist(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        BlacklistURL.objects.create(url=url)
        return redirect('success_page')
    return render(request, 'add_to_blacklist.html')

