from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from ui.forms import (
        RegistrationForm, ProfileEditForm
    )
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

def index(request):
    return HttpResponse("Hello, world. You're at the ui index.")

def home(request):
    name = 'vatsa prahallada'
    nums = ['English', 'Hindi', 'Kannada', 'Tamil', 'Telugu', 'Python', 'C++', 'Perl', 'Shell', 'HTML']
    args = {'name': name, 'numbers': nums}
    return render(request, 'ui/home.html', args)

def login(request):
    pass

def register(request):
    if request.method == 'POST':
        #form = UserCreationForm(request.POST)
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/ui')
    else: # get method
        #form = UserCreationForm()
        form = RegistrationForm()
        args = {'form': form}
        return render(request, 'ui/reg_form.html', args)

#@login_required
def profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    print("User:", user.userprofile.nick_name)
    return render(request, 'ui/profile.html', args)


#@login_required
def profile_edit(request):
    if request.method == 'POST':
        #form = UserChangeForm(request.POST, instance=request.user)
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/ui/profile')
    else: # GET
        #form = UserChangeForm(instance = request.user)
        form = ProfileEditForm(instance = request.user)
        args = {'form': form}
        return render(request, 'ui/profile_edit.html', args)

#@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/ui/profile')
        else:
            return redirect('/ui/change_password')
    else: # GET
        #form = UserChangeForm(instance = request.user)
        form = PasswordChangeForm(user = request.user)
        args = {'form': form}
        return render(request, 'ui/change_password.html', args)
