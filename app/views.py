from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


# Create your views here.

# @login_required(login_url="log_Reg/")
def homeView(request):
    # return render(request, 'app/index.html')
    return render(request, 'app/login_reg.html')

def profileView(request):
    pass

def dashboardView(request):
    return render(request, 'app/index.html')

def loginRegisterView(request):
    return HttpResponse("Logged in")
    return render(request, 'app/login_reg.html')


def logoutView(request):
    logout(request)
    return redirect('logReg')

    

