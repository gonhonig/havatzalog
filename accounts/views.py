from django.shortcuts import render, reverse, redirect
from django.contrib.auth import authenticate, get_user_model, login, logout
from .forms import UserLoginForm, UserRegisterForm


def login_view(request):
    title = 'התחברות'
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect(reverse('panel:selector'))
    return render(request, "accounts/login_form.html", {'form': form, 'title': title})


def register_view(request):
    title = 'הרשמה'
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect(reverse('panel:selector'))

    return render(request, "accounts/register_form.html", {'form': form, 'title': title})


def logout_view(request):
    logout(request)
    return redirect(reverse('index'))