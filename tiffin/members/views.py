from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        remember_me = request.POST.get('remember_me')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if remember_me:
                request.session.set_expiry(1209600)  # 2 Weeks in seconds
            else:
                request.session.set_expiry(0)  # Session ends when browser is closed
            return redirect('home')

        else:
            messages.success(request, "The username and password didn't match!")
            return redirect('login_user')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "You Were Logged Out!")
    return redirect('login_user')