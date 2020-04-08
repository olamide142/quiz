from django.shortcuts import render, HttpResponse, redirect 
from django.contrib.auth.decorators import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
import random 

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
        records = Records.objects.filter(owner=request.user.username)
        history = loggedUser.history.split("***") 
    elif category == 'Doctor':
        loggedUser = Doctor.objects.get(owner=request.user)
        records = {}
        history = {}
    
    context = {'loggedUser':loggedUser, 'Category':category, 'Records': records, 'history':history}
    return render(request, 'app/index.html', context)
    

def uploadView(request):
    pass



def make_recordView(request):
    category = request.session['category']

    if (request.method == 'POST') and (request.session['category'] == 'Doctor'):
        act = request.POST.get('act')
        

        if act == 'search_patient':
            id = request.POST.get('patient_id')
            try:
                patient = Patient.objects.get(id=id)
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
    return render(request, 'app/my_records.html')


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

    dictAge = {'10-19':0, '20-29':0, '30-39':0, '40-49':0, '50-59':0, '60-69':0, '70-79':0, '80-89':0, '90-100' }
    patients = Patient.objects.all()
    for patient in patients:
        age = str(patient.dob).split('/')
        age = calculateAge(date(age[0], age[1], age[2]))
        
        history = str(patient.history).split("***")

        if data in history:
            if (age >= 10) and (age <= 19):
                dictAge['10-19'] += 1
            elif (age >= 20) and (age <= 29):
                dictAge['20-29'] += 1
            elif (age >= 30) and (age <= 39):
                dictAge['30-39'] += 1
            elif (age >= 40) and (age <= 49):
                dictAge['40-49'] += 1
            elif (age >= 50) and (age <= 59):
                dictAge['50-59'] += 1
            elif (age >= 60) and (age <= 69):
                dictAge['60-69'] += 1
            elif (age >= 70) and (age <= 79):
                dictAge['70-79'] += 1
            elif (age >= 80) and (age <= 89):
                dictAge['80-89'] += 1
            elif (age >= 90) and (age <= 100):
                dictAge['90-100'] += 1

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


            
                
        





# from datetime import date 
  
# def calculateAge(born): 
#     today = date.today() 
#     try:  
#         birthday = born.replace(year = today.year) 
#     except ValueError:  
#         birthday = born.replace(year = today.year, 
#                   month = born.month + 1, day = 1) 
  
#     if birthday > today: 
#         return today.year - born.year - 1
#     else: 
#         return today.year - born.year 
          
# print(calculateAge(date(1997, 2, 3)), "years") 
















































# def fake(request):
        
#     surname = [
#     "Aaran",
#     "Aaren",
#     "Aarez",
#     "Aarman",
#     "Aaron",
#     "Aaron-James",
#     "Aarron",
#     "Aaryan",
#     "Aaryn",
#     "Aayan",
#     "Aazaan",
#     "Abaan",
#     "Abbas",
#     "Abdallah",
#     "Abdalroof",
#     "Abdihakim",
#     "Abdirahman",
#     "Abdisalam",
#     "Abdul",
#     "Abdul-Aziz",
#     "Abdulbasir",
#     "Abdulkadir",
#     "Abdulkarem",
#     "Abdulkhader",
#     "Abdullah",
#     "Abdul-Majeed",
#     "Abdulmalik",
#     "Abdul-Rehman",
#     "Abdur",
#     "Abdurraheem",
#     "Abdur-Rahman",
#     "Abdur-Rehmaan",
#     "Abel",
#     "Abhinav",
#     "Abhisumant",
#     "Abid",
#     "Abir",
#     "Abraham",
#     "Abu",
#     "Abubakar",
#     "Ace",
#     "Adain",
#     "Adam",
#     "Adam-James",
#     "Addison",
#     "Addisson",
#     "Adegbola",
#     "Adegbolahan",
#     "Aden",
#     "Adenn",
#     "Adie",
#     "Adil",
#     "Aditya",
#     "Adnan",
#     "Adrian",
#     "Adrien",
#     "Aedan",
#     "Aedin",
#     "Aedyn",
#     "Aeron",
#     "Afonso",
#     "Ahmad",
#     "Ahmed",
#     "Ahmed-Aziz",
#     "Ahoua",
#     "Ahtasham",
#     "Aiadan",
#     "Aidan",
#     "Aiden",
#     "Aiden-Jack",
#     "Aiden-Vee",
#     "Aidian",
#     "Aidy",
#     "Ailin",
#     "Aiman",
#     "Ainsley",
#     "Ainslie",
#     "Airen",
#     "Airidas",
#     "Airlie",
#     "AJ",
#     "Ajay",
#     "A-Jay",
#     "Ajayraj",
#     "Akan",
#     "Akram",
#     "Thierry",
#     "Thom",
#     "Thomas",
#     "Thomas-Jay",
#     "Thomson",
#     "Thorben",
#     "Thorfinn",
#     "Zohaib",
#     "Zohair",
#     "Zoubaeir",
#     "Zoza",
#     "Zubair",
#     "Zubayr",
#     "Zuriel"
#     ]

#     other_names = ["Cadyn",
#     "Caedan",
#     "Caedyn",
#     "Cael",
#     "Caelan",
#     "Caelen",
#     "Caethan",
#     "Cahl",
#     "Cahlum",
#     "Cai",
#     "Caidan",
#     "Caiden",
#     "Caiden-Paul",
#     "Caidyn",
#     "Caie",
#     "Cailaen",
#     "Cailean",
#     "Caileb-John",
#     "Cailin",
#     "Cain",
#     "Caine",
#     "Cairn",
#     "Cal",
#     "Calan",
#     "Calder",
#     "Cale",
#     "Calean",
#     "Caleb",
#     "Calen",
#     "Caley",
#     "Calib",
#     "Calin",
#     "Callahan",
#     "Callan",
#     "Callan-Adam",
#     "Calley",
#     "Callie",
#     "Callin",
#     "Callum",
#     "Callun",
#     "Callyn",
#     "Calum",
#     "Calum-James",
#     "Calvin",
#     "Cambell",
#     "Camerin",
#     "Cameron",
#     "Campbel",
#     "Campbell",
#     "Camron",
#     "Caolain",
#     "Caolan",
#     "Carl",
#     "Carlo",
#     "Carlos",
#     "Carrich",
#     "Carrick",
#     "Carson",
#     "Carter",
#     "Carwyn",
#     "Casey",
#     "Casper",
#     "Cassy",
#     "Cathal",
#     "Cator",
#     "Cavan",
#     "Cayden",
#     "Cayden-Robert",
#     "Cayden-Tiamo",
#     "Ceejay",
#     "Ceilan",
#     "Ceiran",
#     "Ceirin",
#     "Ceiron",
#     "Cejay",
#     "Celik",
#     "Cephas",
#     "Cesar",
#     "Cesare",
#     "Chad",
#     "Chaitanya",
#     "Chang-Ha",
#     "Charles",
#     "Charley",
#     "Charlie",
#     "Christopher",
#     "Christopher-Lee",
#     "Christy",
#     "Chu",
#     "Chukwuemeka",
#     "Cian",
#     "Ciann",
#     "Ciar",
#     "Codi",
#     "Codie",
#     "Cormack",
#     "Cormak",
#     "Corran",
#     "Corrie",
#     "Cory",]

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


#     patient_status = [
#             ('Great', 'Great'),
#             ('Good', 'Good'),
#             ('Not so good', 'Not so good'),
#             ('Recovering', 'Recovering'),
#             ('Bad', 'Bad')]
#     year = [2000, 1988, 1982, 1963, 1970, 1956, 1977, 1998, 1987, 1993, 1991, 1997, 1984]
#     month = [1,2,3,4,5,6,7,8,9,10,11,12]
#     day = [2,5,22,6,7,8,9,18]

#     for i in range(100):
#         user = User.objects.get(username='patient'+str(i)+'@abc.com')
#         x = random.choice(case) 
#         y = random.choice(case) 
#         z = random.choice(case) 
#         xx = str(x[0])+"***"+str(y[0])+"***"+str(z[0])
#         p = Patient.objects.get(owner=user)
#         p.status = xx

#         p.save()

#     return HttpResponse("Done!!!")