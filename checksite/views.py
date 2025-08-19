from django.shortcuts import render

# Create your views here.
def check_site(request):
    return render(request,'check_site.html')