from django.shortcuts import render, HttpResponse, redirect 
from django.contrib.auth.decorators import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
import random 

from . models import * 
from .forms import UploadFileForm

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
                        request.session['category'] = request.POST['category']
                elif request.session['category'] == 'Doctor':
                    # return HttpResponse(Doctor.objects.get(owner=user))
                    if Doctor.objects.get(owner=user) is not None:
                        login(request, user)
                        request.session['category'] = request.POST['category']
                
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
    


def signupView(request):
    if request.method == "POST":
        category = request.POST.get('category')
        email = request.POST.get('email')
        surname = request.POST.get('surname')
        other_names = request.POST.get('other_names')
        gender = request.POST.get('gender')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if category == 'Doctor':
                user = User.objects.create_user(username=email, password=password1)
                
                specialization = request.POST.get('specialization')
                doctor = Doctor.objects.create(owner=user, surname=surname, other_names=other_names, specialization=specialization, gender=gender)
                doctor.save()
                messages.add_message(request, messages.INFO, 'Account created successfully')
                return render(request, 'app/signup.html')
                
            elif category == 'Patient':
                user = User.objects.create_user(username=email, password=password1)
                patient = Patient.objects.create(owner=user, surname=surname, other_names=other_names, gender=gender)
                patient.save()
                messages.add_message(request, messages.INFO, 'Account created successfully')
                return render(request, 'app/login.html')
        else:
            messages.add_message(request, messages.INFO, 'Password are not the same')
            return render(request, 'app/login.html')
            

    return render(request, "app/signup.html")





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
            loggedUser = Patient.objects.get(owner=request.user)
            loggedUser.surname=surname
            loggedUser.other_names=other_names
            loggedUser.phone_number=phone_number
            loggedUser.gender=gender
            loggedUser.home_address=home_address
            loggedUser.dob=dob
            loggedUser.marital_status=marital_status
            loggedUser.next_of_kin=next_of_kin
            loggedUser.next_of_kin_addr=next_of_kin_addr
            loggedUser.next_of_kin_no=next_of_kin_no
            loggedUser.genotype=genotype
            loggedUser.blood_group=blood_group
            loggedUser.weight=weight
            loggedUser.status=status
            loggedUser.save()

            # Get Patient history and store seperately
            history = loggedUser.history.split("***")   
            loggedUser.id = loggedUser.patient_id

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
            loggedUser.id = loggedUser.doctor_id

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
            loggedUser.id = loggedUser.patient_id

        elif category == 'Doctor':
            loggedUser = Doctor.objects.get(owner=owner)
            loggedUser.id = loggedUser.doctor_id
            context = {'loggedUser':loggedUser, 'Category':category}
        
        return render(request, 'app/profile.html', context)


@login_required(login_url="login/")
def dashboardView(request):

    category = request.session['category']

    # Get users info 
    if category == 'Patient':
        loggedUser = Patient.objects.get(owner=request.user)
        records = Records.objects.filter(owner=request.user.username)
        history = loggedUser.history.split("***")

        # This ridiculous section handles image rending to the template 
        a = (loggedUser.image).replace("___"+str(request.user.username), "")
        loggedUser.image = "/static/app/profilepic/"+str(a)
        loggedUser.id = loggedUser.patient_id
    elif category == 'Doctor':
        loggedUser = Doctor.objects.get(owner=request.user)
        records = {}
        history = {}
        loggedUser.id = loggedUser.doctor_id

        # This ridiculous section handles image rending to the template 
        a = (loggedUser.image).replace("___"+str(request.user.username), "")
        loggedUser.image = "/static/app/profilepic/"+str(a)
        loggedUser.id = loggedUser.patient_id

    context = {'loggedUser':loggedUser, 'Category':category, 'Records': records, 'history':history}


    return render(request, 'app/index.html', context)
    


def make_recordView(request):
    category = request.session['category']

    if (request.method == 'POST') and (request.session['category'] == 'Doctor'):
        act = request.POST.get('act')
        

        if act == 'search_patient':
            id = request.POST.get('patient_id')
            try:
                patient = Patient.objects.get(patient_id=id)
            except:
                messages.add_message(request, messages.INFO, 'No record found')
                return render(request, 'app/make_record.html')
            
            if patient is not None:
                history = str(patient.history).split("***")
                context = {'patient':patient, 'history':history}
                messages.add_message(request, messages.INFO, 'Add Record for Patient: '+str(patient))
                return render(request, 'app/make_record.html', context)

        elif act == 'upload_record':
            patient = request.POST.get('id')
            # patient = User.objects.get(username=patient)
            # patient = Patient.objects.get(owner=patient)
            symptoms = request.POST.get('Symptoms')
            description = request.POST.get('Description')
            doctor = request.user.username
            # doctor = Doctor.objects.get(owner=doctor)
            doctors_report = request.POST.get('Doctors_report')
            status = request.POST.get('status')

            record = Records.objects.create(owner=patient, symptoms=symptoms,
            description=description, doctor=doctor, doctors_report=doctors_report,
            status=status)

            record.save()
            messages.add_message(request, messages.INFO, 'Record was successfully Added for Patient')
            context = {'Category':category}
            return render(request, 'app/make_record.html', context)

    else:
        # GET REQUEST 
        context = {'Category':category}
        return render(request, 'app/make_record.html', context)



def recordsView(request, id):
    record = Records.objects.get(record_id=id)
    patient = User.objects.get(username=record.owner)
    patient = Patient.objects.get(owner=patient)
    history = patient.history.split("***")
    category = request.session['category']

    context = {'record':record, 'history':history, 'Category':category, 'patient':patient}

    return render(request, 'app/records.html', context)




def myRecordsView(request):
    pass


def uploadView(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])

        category = request.session['category']

        file_owner = str(request.user)

        user = User.objects.get(username=file_owner)
        upload_file = request.FILES['file']

        if category == 'Patient':
            patient = Patient.objects.get(owner=user)
            patient.image = str(upload_file.name)+"___"+str(file_owner)
            patient.save()

        elif category == 'Doctor':
            doctor = Doctor.objects.get(owner=user)
            doctor.image = str(upload_file.name)+"___"+str(file_owner)
            doctor.save()


        return redirect('dashboard')   
    else:
        return JsonResponse({'file_id': "Something went wrong"})


def handle_uploaded_file(f):
    with open('static/app/profilepic/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)



def tableView(request):
    
    category = request.session['category']
    if category != 'Doctor':
        redirect('dashboard')
    if request == "POST":
        return HttpResponse("Search Table")
    return render(request, 'app/table.html')


def chartView(request):
    if request.method == 'POST':
        data = request.POST.get('data')
    else:
        data = 'HIV/AIDS'

    dictAge = {'one':0, 'two':0, 'three':0, 'four':0, 'five':0, 'six':0, 'seven':0, 'eight':0, 'nine':0}
    patients = Patient.objects.all()
    for patient in patients:
        if '/' in str(patient.dob):
            age = str(patient.dob).split('/')
        else:
            age = str(patient.dob).split('-')

        age = calculateAge(date(int(age[0]*1), int(age[1]*1), int(age[2]*1)))
        
        history = str(patient.history)

        if data in history:
            if (age >= 10) and (age <= 19):
                dictAge['one'] += 1
            elif (age >= 20) and (age <= 29):
                dictAge['two'] += 1
            elif (age >= 30) and (age <= 39):
                dictAge['three'] += 1
            elif (age >= 40) and (age <= 49):
                dictAge['four'] += 1
            elif (age >= 50) and (age <= 59):
                dictAge['five'] += 1
            elif (age >= 60) and (age <= 69):
                dictAge['six'] += 1
            elif (age >= 70) and (age <= 79):
                dictAge['seven'] += 1
            elif (age >= 80) and (age <= 89):
                dictAge['eight'] += 1
            elif (age >= 90) and (age <= 100):
                dictAge['nine'] += 1
    
    context = {'dictAge':dictAge}

    return render(request, 'app/chart.html', dictAge)



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


            
                
        





from datetime import date 
  
def calculateAge(born): 
    today = date.today() 
    try:  
        birthday = born.replace(year = today.year) 
    except ValueError:  
        birthday = born.replace(year = today.year, 
                  month = born.month + 1, day = 1) 
  
    if birthday > today: 
        return today.year - born.year - 1
    else: 
        return today.year - born.year 
          
# print(calculateAge(date(1997, 2, 3)), "years") 
















































# def fake(request):

#     case =[
#         ('ADHD', 'ADHD'),
#         ('Arthritis', 'Arthritis'),
#         ('Asthma', 'Asthma'),
#         ('Autism', 'Autism'),
#         ('Birth Defects', 'Birth Defects'),
#         ('Cancer', 'Cancer'),
#         ('Cattarh', 'Cattarh'),
#         ('Coughing', 'Coughing'),
#         ('Diarrhoea', 'Diarrhoea'),
#         ('Chlamydia', 'Chlamydia'),
#         ('Chronic Obstructive Pulmonary Disease (COPD)', 'Chronic Obstructive Pulmonary Disease (COPD)'),
#         ('Coronavirus Disease (COVID-19)', 'Coronavirus Disease (COVID-19)'),
#         ('Diabetes', 'Diabetes'),
#         ('Ebola (Ebola Virus Disease)', 'Ebola (Ebola Virus Disease)'),
#         ('Epilepsy', 'Epilepsy'),
#         ('Flu (Influenza)', 'Flu (Influenza)'),
#         ('Genital Herpes (Herpes Simplex Virus)', 'Genital Herpes (Herpes Simplex Virus)'),
#         ('Gonorrhea', 'Gonorrhea'),
#         ('Heart Disease', 'Heart Disease'),
#         ('Headache', 'Headache'),
#         ('Hepatitis', 'Hepatitis'),
#         ('HIV/AIDS', 'HIV/AIDS'),
#         ('Kidney Disease (Chronic Kidney Disease)', 'Kidney Disease (Chronic Kidney Disease)'),
#         ('Lassa Fever', 'Lassa Fever'),
#         ('Meningitis', 'Meningitis'),
#         ('Parasites – Scabies', 'Parasites – Scabies'),
#         ('Salmonella', 'Salmonella'),
#         ('Sexually Transmitted Diseases', 'Sexually Transmitted Diseases'),
#         ('Surgical Operation', 'Surgical Operation'),
#         ('Stroke', 'Stroke'),
#         ('Traumatic Brain Injury (TBI)', 'Traumatic Brain Injury (TBI)'),
#         ('Tuberculosis (TB)', 'Tuberculosis (TB)'),
#         ('Typhoid', 'Typhoid'),
#         ('Zika Virus', 'Zika Virus')
#     ]


#     year = [2000, 1988, 1982, 1963, 1970, 1956, 1977, 1998, 1987, 1993, 1991, 1997, 1984]
#     month = [1,2,3,4,5,6,7,8,9,10,11,12]
#     day = [2,5,22,6,7,8,9,18]

#     for i in range(100):
#         user = User.objects.get(username='patient'+str(i)+'@abc.com')
#         x = random.choice(case)
#         y = random.choice(case) 
#         z = random.choice(case) 
#         xx = str(x)+"***"+str(y)+"***"+str(z)
#         # return HttpResponse(xx)
#         p = Patient.objects.get(owner=user)
#         p.history = xx

#         p.save()

#     return HttpResponse("Done!!!")