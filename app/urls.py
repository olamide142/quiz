from django.urls import path, reverse
from . import views

urlpatterns = [
    path('', views.dashboardView, name="dashboard"),
    path('login/', views.loginView, name="login"),
    path('signup/', views.signupView, name="signup"),
    path('records/<str:id>', views.recordsView, name="records"),
    path('records/', views.myRecordsView, name="my_records"),
    path('make_record/', views.make_recordView, name="make_record"),
    path('report_pdf/', views.report_pdfView, name="report_pdf"),
    path('table/', views.tableView, name="table"),
    path('chart/', views.chartView, name="chart"),
    path('profile/', views.profileView, name="profile"),
    path('upload/', views.uploadView, name="upload"),
    path('logout/', views.logoutView, name="logout"),
    path('initial_data/', views.initial_dataView, name="initial_data"),

]