# Generated by Django 3.0.2 on 2020-04-08 14:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Records',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_id', models.CharField(default='9uyIG7Mbo6', max_length=10)),
                ('owner', models.CharField(blank=True, max_length=50, null=True)),
                ('symptoms', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('doctor', models.CharField(blank=True, max_length=50, null=True)),
                ('doctors_report', models.TextField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('Resolved', 'Resolved'), ('Recovering', 'Recovering'), ('Examination', 'Examination'), ('Critical', 'Critical')], max_length=15, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_id', models.CharField(default='G8zjPE76lY', max_length=10, null=True)),
                ('image', models.CharField(blank=True, max_length=50, null=True)),
                ('surname', models.CharField(max_length=50, null=True)),
                ('other_names', models.CharField(max_length=50, null=True)),
                ('status', models.CharField(choices=[('Great', 'Great'), ('Good', 'Good'), ('Not so good', 'Not so good'), ('Recovering', 'Recovering'), ('Bad', 'Bad')], max_length=50, null=True)),
                ('gender', models.CharField(blank=True, max_length=6, null=True)),
                ('phone_number', models.BigIntegerField(default=0, null=True)),
                ('history', models.TextField(blank=True, default='')),
                ('weight', models.IntegerField(default=0, null=True)),
                ('blood_group', models.CharField(blank=True, choices=[('A', 'A'), ('A+', 'A+'), ('B', 'B'), ('B+', 'B+'), ('AB', 'AB'), ('AB+', 'AB+'), ('O', 'O'), ('O+', 'O+')], max_length=3, null=True)),
                ('genotype', models.CharField(blank=True, max_length=5, null=True)),
                ('home_address', models.CharField(blank=True, max_length=300, null=True)),
                ('dob', models.CharField(blank=True, max_length=10, null=True)),
                ('marital_status', models.CharField(blank=True, max_length=15, null=True)),
                ('next_of_kin', models.CharField(blank=True, max_length=30, null=True)),
                ('next_of_kin_no', models.IntegerField(default=0, null=True)),
                ('next_of_kin_addr', models.CharField(blank=True, max_length=30, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('owner', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor_id', models.CharField(default='xM1a2htujK', max_length=10, null=True)),
                ('image', models.CharField(blank=True, max_length=50, null=True)),
                ('surname', models.CharField(max_length=50, null=True)),
                ('other_names', models.CharField(max_length=50, null=True)),
                ('gender', models.CharField(blank=True, max_length=6, null=True)),
                ('specialization', models.CharField(blank=True, max_length=25, null=True)),
                ('phone_number', models.BigIntegerField(default=0, null=True)),
                ('years_of_experience', models.IntegerField(default=0, null=True)),
                ('home_address', models.CharField(blank=True, max_length=300, null=True)),
                ('dob', models.CharField(blank=True, max_length=10, null=True)),
                ('marital_status', models.CharField(blank=True, max_length=15, null=True)),
                ('next_of_kin', models.CharField(blank=True, max_length=30, null=True)),
                ('next_of_kin_no', models.IntegerField(default=0, null=True)),
                ('next_of_kin_addr', models.CharField(blank=True, max_length=30, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('owner', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
