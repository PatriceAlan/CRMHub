from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

def home(request):
    search_query = request.GET.get('search_query')
    records = Record.objects.all()

    if search_query:
        # Effectuez la recherche uniquement si un terme de recherche est fourni
        records = records.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful. Welcome back!")
            return redirect('home')
        else:
            messages.error(request, "Login Failed. Please check your credentials and try again...")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records, 'search_query': search_query})

def logout_user(request):
    logout(request)
    messages.success(request, "Logout Successful. Don't hesitate to come again!")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration Successful! You can now log in using your credentials.")
            return redirect('home')
    else:
        form = SignUpForm()
    
    return render(request, 'register.html', {'form': form})

def user_record(request, pk):
    if request.user.is_authenticated:
        user_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'user_record': user_record})
    else:
        messages.error(request, "You must be logged in to view that page...")
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record deleted successfully!")
        return redirect('home')
    else:
        messages.error(request, "You must be logged in to view that page...")
        return redirect('home')

def add_record(request):
    user_form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if user_form.is_valid():
                add_record = user_form.save()
                messages.success(request, "Record added successfully!")
                return redirect('home')
        return render(request, 'add_record.html', {'form': user_form})
    else:
        messages.error(request, "You must be logged in to view that page...")
        return redirect('home')

def update_record(request, pk):
	if request.user.is_authenticated:
		current_record = Record.objects.get(id=pk)
		user_form = AddRecordForm(request.POST or None, instance=current_record)
		if user_form.is_valid():
			user_form.save()
			messages.success(request, "Record Has Been Updated!")
			return redirect('home')
		return render(request, 'update_record.html', {'form':user_form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')

