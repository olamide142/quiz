from django.db import models
from django.contrib.auth.models import User

# Create your models here.

import random
def randomId():
    characters = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""
    for i in range(10):
        result += characters[random.randrange(len(characters))]
    return result

class Doctor(models.Model):
    doctor_id = models.CharField(default=randomId(), primary_key=True, max_length=10)
    owner = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    image = models.CharField(max_length=50, null=True, blank=True)
    surname = models.CharField(max_length=50, null=True)
    other_names = models.CharField(max_length=50, null=True)
    gender = models.CharField(max_length=6, null=True, blank=True)
    specialization = models.CharField(max_length=25, null=True, blank=True)
    phone_number = models.BigIntegerField(default=0, null=True)
    years_of_experience = models.IntegerField(default=0, null=True)
    home_address = models.CharField(max_length=300, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    marital_status = models.CharField(max_length=15, null=True, blank=True)
    next_of_kin =  models.CharField(max_length=30, null=True, blank=True)
    next_of_kin_addr =  models.CharField(max_length=30, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null = True)

    def __str__(self):
        return self.surname +'. '+str(self.other_names[0])


class Patient(models.Model):
    GENOTYPE = (
            ('AA', 'AA'),
            ('AS', 'AS'),
            ('SS', 'SS'),
            ('AC', 'AC')
    )
    BLOOD_GROUP = (
            ('A', 'A'),
            ('A+', 'A+'),
            ('B', 'B'),
            ('B+', 'B+'),
            ('AB', 'AB'),
            ('AB+', 'AB+'),
            ('O', 'O'),
            ('O+', 'O+')
    )

    STATUS = (
            ('Great', 'Great'),
            ('Good', 'Good'),
            ('Not so good', 'Not so good'),
            ('Recovering', 'Recovering'),
            ('Bad', 'Bad')
    )
    patient_id = models.CharField(default=randomId(), primary_key=True,  max_length=10)
    owner = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    image = models.CharField(max_length=50, null=True, blank=True)
    surname = models.CharField(max_length=50, null=True)
    other_names = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, choices=STATUS, null=True)
    gender = models.CharField(max_length=6, null=True, blank=True)
    phone_number = models.BigIntegerField(null=True, default=0)
    weight = models.IntegerField(null=True, default=0)
    blood_group =  models.CharField(max_length=3, choices=BLOOD_GROUP, null=True, blank=True)
    genotype =  models.CharField(max_length=5, null=True, blank=True)
    home_address = models.CharField(max_length=300, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    marital_status = models.CharField(max_length=15, null=True, blank=True)
    next_of_kin =  models.CharField(max_length=30, null=True, blank=True)
    next_of_kin_addr =  models.CharField(max_length=30, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null = True)

    def __str__(self):
        return self.surname +'. '+str(self.other_names)

    
class Records(models.Model):
    STATUS = (
            ('Resolved', 'Resolved'),
            ('Recovering', 'Recovering'),
            ('Examination', 'Examination'),
            ('Critical', 'Critical')
    )
    record_id = models.CharField(default=randomId(), primary_key=True,  max_length=10)
    owner = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    symptoms = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    doctor = models.OneToOneField(Doctor, null=True, on_delete=models.SET_NULL)
    doctors_report =  models.TextField(null=True, blank=True)
    status = models.CharField(null=True, blank=True, choices=STATUS, max_length=15)
    date_created = models.DateTimeField(auto_now_add=True, null = True)


    def __str__(self):
        return str(owner) +'-'+ str(record_id)

class Case(models.Model):
    CATEGORY = (
        ('ADHD', 'ADHD'),
        ('Arthritis', 'Arthritis'),
        ('Asthma', 'Asthma'),
        ('Autism', 'Autism'),
        ('Birth Defects', 'Birth Defects'),
        ('Cancer', 'Cancer'),
        ('Cattarh', 'Cattarh'),
        ('Coughing', 'Coughing'),
        ('Diarrhoea', 'Diarrhoea'),
        ('Chlamydia', 'Chlamydia'),
        ('Chronic Obstructive Pulmonary Disease (COPD)', 'Chronic Obstructive Pulmonary Disease (COPD)'),
        ('Coronavirus Disease (COVID-19)', 'Coronavirus Disease (COVID-19)'),
        ('Diabetes', 'Diabetes'),
        ('Ebola (Ebola Virus Disease)', 'Ebola (Ebola Virus Disease)'),
        ('Epilepsy', 'Epilepsy'),
        ('Flu (Influenza)', 'Flu (Influenza)'),
        ('Genital Herpes (Herpes Simplex Virus)', 'Genital Herpes (Herpes Simplex Virus)'),
        ('Gonorrhea', 'Gonorrhea'),
        ('Heart Disease', 'Heart Disease'),
        ('Headache', 'Headache'),
        ('Hepatitis', 'Hepatitis'),
        ('HIV/AIDS', 'HIV/AIDS'),
        ('Kidney Disease (Chronic Kidney Disease)', 'Kidney Disease (Chronic Kidney Disease)'),
        ('Lassa Fever', 'Lassa Fever'),
        ('Meningitis', 'Meningitis'),
        ('Parasites – Scabies', 'Parasites – Scabies'),
        ('Salmonella', 'Salmonella'),
        ('Sexually Transmitted Diseases', 'Sexually Transmitted Diseases'),
        ('Surgical Operation', 'Surgical Operation'),
        ('Stroke', 'Stroke'),
        ('Traumatic Brain Injury (TBI)', 'Traumatic Brain Injury (TBI)'),
        ('Tuberculosis (TB)', 'Tuberculosis (TB)'),
        ('Typhoid', 'Typhoid'),
        ('Zika Virus', 'Zika Virus')
    )
    owner = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    record = models.ForeignKey(Records, on_delete=models.CASCADE)
    case = models.CharField(null=True, blank=True, choices=CATEGORY, max_length=50)
    date_created = models.DateTimeField(auto_now_add=True, null = True)

    
    def __str__(self):
        return str(record)+'-'+str(case)


