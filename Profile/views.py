from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required



@login_required
def profile(request):
    return render(request, 'profile.html')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm
from .models import UserProfile

@login_required
def update_user_info(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data.get('new_password')
            if password:
                user.set_password(password)
            user.save()
            
            # check if user has a profile object
            if hasattr(request.user, 'profile'):
                request.user.profile.save()
            else:
                # create a new profile object if one does not exist
                profile = UserProfile(user=request.user)
                profile.save()
                
            messages.success(request, 'Your profile has been updated!')
            return redirect('home')
    else:
        user_form = UserUpdateForm(instance=request.user)

    context = {
        'user_form': user_form,
    }
    return render(request, 'profile.html', context)
