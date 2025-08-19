from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def register(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if pass1 != pass2:
            return HttpResponse('password does not match')
        else:
            my_user = User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
    return render(request,'signup.html')
def Login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request,username = username,password = pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            HttpResponse('user name or password is incorrect')
    return render(request,'login.html')



def Logout(request):
    if 'username' in request.session:
        del request.session['username']
    logout(request)
    return redirect('home')
