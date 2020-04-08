from django.shortcuts import render, HttpResponse, redirect 
from django.contrib.auth.decorators import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from . models import * 

# Create your views here.



def loginView(request):
    if request.method == 'POST':

        # Store category of user in session
        request.session['category'] = request.POST['category']
        
        # Get email and password
        username = request.POST['email']
        password = request.POST['password']


        # Authenticate user and log them in 
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # check if user is a really who they say they are 
            # wrapping in a try catch to handle error incase user 
            # is not who they say they are
            try:
                if request.session['category'] == 'Patient':
                    if Patient.objects.get(owner=user) is not None:
                        login(request, user)
                elif request.session['category'] == 'Doctor':
                    # return HttpResponse(Doctor.objects.get(owner=user))
                    if Doctor.objects.get(owner=user) is not None:
                        login(request, user)
                
                messages.add_message(request, messages.INFO, 'Welcome Back 😎')
                return redirect('dashboard')
            except:
                messages.add_message(request, messages.WARNING, 'You are not a '+str(request.session['category']))
                return render(request, 'app/login.html')

        else:
        # if user does not exist return back
        #  to login page and display error message 
            messages.add_message(request, messages.WARNING, 'Invalid Login Details')
            return render(request, 'app/login.html')

    # GET REQUEST 
    return render(request, 'app/login.html')
    

def logoutView(request):
    # Log user out
    logout(request)
    return redirect('dashboard')



@login_required(login_url="login/")
def profileView(request):

    # Get logged in user's details
    owner = request.user
    category = request.session['category']

    if request.method == 'POST':
            # General profile info of both Dotors and Patients
        surname = request.POST.get('Surname')
        other_names = request.POST.get('otherNames')
        phone_number = request.POST.get('phoneNumber')
        gender = request.POST.get('gender')
        home_address = request.POST.get('address')
        dob = request.POST.get('dob')
        marital_status = request.POST.get('maritalStatus')
        next_of_kin =  request.POST.get('next_of_kin')
        next_of_kin_addr = request.POST.get('next_of_kin_address')
        next_of_kin_no = request.POST.get('next_of_kin_no')

            # if User is a Patient 
        if category == 'Patient':
            genotype =  request.POST.get('genotype')
            blood_group = request.POST.get('bloodGroup')
            weight = request.POST.get('weight')
            status = request.POST.get('status')

            # Update Patient's profile
            loggedUser = Patient.objects.filter(owner=request.user).update(
                surname=surname, other_names=other_names, phone_number=phone_number,
                gender=gender, home_address=home_address, dob=dob,
                marital_status=marital_status, next_of_kin=next_of_kin, next_of_kin_addr=next_of_kin_addr,
                next_of_kin_no=next_of_kin_no, genotype=genotype, blood_group=blood_group,
                weight=weight, status=status
                )
                # Get Patient history and store seperately
            history = str(loggedUser.history).split("***")


            # if User is a Doctor
        elif category == 'Doctor':
            specialization = request.POST.get('specialization')
            years_of_experience = request.POST.get('years_of_experience')

            # Update Doctor's profile
            loggedUser = Doctor.objects.filter(owner=request.user).update(
                surname=surname, other_names=other_names, phone_number=phone_number,
                gender=gender, home_address=home_address, dob=dob,
                marital_status=marital_status, next_of_kin=next_of_kin, next_of_kin_addr=next_of_kin_addr,
                next_of_kin_no=next_of_kin_no, specialization=specialization, years_of_experience=years_of_experience
                )
            history = []

        # if user chooses to change his email address
        email = request.POST.get('email')
        user = User.objects.get(username=str(owner.username))
        user.username = email
        user.save()

        # store a the loggedUser object in a dict 
        context = {'loggedUser':loggedUser, 'Category':category, 'history':history}

        return redirect('profile')

    else:
        # When request method is GET 
        # Get users info
        context = {}
        if category == 'Patient':
            loggedUser = Patient.objects.get(owner=owner)
            history = str(loggedUser.history).split("***")
            context = {'loggedUser':loggedUser, 'Category':category, 'history':history}
        elif category == 'Doctor':
            loggedUser = Doctor.objects.get(owner=owner)
            context = {'loggedUser':loggedUser, 'Category':category}
        
        return render(request, 'app/profile.html', context)


@login_required(login_url="login/")
def dashboardView(request):

    category = request.session['category']

    # Get users info 
    if category == 'Patient':
        loggedUser = Patient.objects.get(owner=request.user)
    elif category == 'Doctor':
        loggedUser = Doctor.objects.get(owner=request.user)
    
    context = {'loggedUser':loggedUser, 'Category':category}
    return render(request, 'app/index.html', context)
    

def uploadView(request):
    pass



def make_recordView(request):
    if (request.method == 'POST') and (request.session['category'] == 'Doctor'):
        if request.POST.act == 'search_patient':
            id = request.POST.get('patient_id')
            patient = Patient.objects.get(id=id)
            if patient is not None:
                context = {'patient':patient}
                messages.add_message(request, messages.INFO, 'Add Record for Patient: '+str(patient))
                return (request, 'app/make_record.html', context)
            else:
                messages.add_message(request, messages.INFO, 'No record found')
                return (request, 'app/make_record.html', context)

        elif request.POST.act == 'upload_record':
            pass
    else:
        return redirect('dashboard')


    return render(request, 'app/make_record.html')



def recordsView(request):
    return render(request, 'app/records.html')


def tableView(request):
    
    category = request.session['category']
    if category != 'Doctor':
        redirect('dashboard')
    if request == "POST":
        return HttpResponse("Search Table")
    return render(request, 'app/table.html')


def chartView(request):
    return render(request, 'app/chart.html')


def report_pdfView(request):
    return render(request, 'app/report_pdf.html')


    

def initial_dataView(request):
    if request.method == 'POST':
        _li = ""
        # text = 

        textArr = request.POST.get('history').split('***')
        textDict = dict()
        for i in textArr:
            textDict[i] = 0

        
        for t in textArr:
            textDict[t] += 1

        for dic in textDict:
            if (textDict[dic] % 2 != 0) or (textDict[dic] == 1):
                _li = _li+""+str(dic)+"***"
        
        patient = Patient.objects.get(owner=request.user)
        patient.history = _li
        patient.save()
        return redirect('profile')


            
                
          