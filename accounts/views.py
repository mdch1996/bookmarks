from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

from .forms import LoginForm, UserRegistrationForm
from .models import Profile


def user_login(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print("--------uncleaned_data-------", form)
            cd = form.cleaned_data
            print("--------cleaned_data-------", cd)
            user = authenticate(username=cd['username'], password=cd['password'])
            print("--------authenticate-------", user)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        print("request.POST", request.POST)
        print("------user-form------", user_form)
        if user_form.is_valid():

            new_user = user_form.save(commit=False)

            print("------user_form.save------", new_user)
            new_user.set_password(user_form.cleaned_data['password'])
            print("------user_form..user_form------", new_user)
            # new_user.save()
            # profile = Profile.objects.create(user=new_user)
            return render(request,
                          'accounts/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'user_form': user_form})

