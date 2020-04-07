from django.shortcuts import render, HttpResponse, redirect 
from django.contrib.auth.decorators import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages



# Create your views here.
class Category(object):
    category = ''


def loginView(request):
    print(f"REQUEST TYPE: {request.method}")
    if request.method == 'POST':

        # Store category of user in the category class
        category = request.POST['category']
        if category == 'Patient':
            Category.category = 'Patient'
        elif category == 'Doctor':
            Category.category = 'Doctor'

        # Get email and password
        username = request.POST['email']
        password = request.POST['password']

        # Authenticate user and log them in 
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.INFO, 'Welcome Back 😎')
            return redirect('dashboard')
        else:
        # if user does not exist return back
        #  to login page and display error message 
            messages.add_message(request, messages.WARNING, 'Invalid Login Details')
            return render(request, 'app/login.html')

    # GET REQUEST 
    return render(request, 'app/login.html')
    

def logoutView(request):
    logout(request)
    return redirect('home')


@login_required(login_url="login/")
def homeView(request):
    return render(request, 'app/index.html')


def profileView(request):
    return render(request, 'app/profile.html')


def dashboardView(request):
    return render(request, 'app/index.html')
    

def uploadView(request):
    pass


def recordsView(request):
    return render(request, 'app/records.html')


def tableView(request):
    if request == "POST":
        return HttpResponse("Search Table")
    return render(request, 'app/table.html')


def chartView(request):
    return render(request, 'app/chart.html')


def report_pdfView(request):
    return render(request, 'app/report_pdf.html')


    

