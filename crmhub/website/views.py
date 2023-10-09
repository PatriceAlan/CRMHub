from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    # Verify if user is logged in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authentication
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful!")
            return redirect('home')
        else:
            messages.success(request, "Login Failed. Please check your credentials and try again...")
            return redirect('home')
    else:
        return render(request, 'home.html', {})

def logout_user(request):
    pass