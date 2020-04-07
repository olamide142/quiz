from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeView, name="home"),
    path('login/', views.loginView, name="login"),
    path('dashboard/', views.dashboardView, name="dashboard"),
    path('records/', views.recordsView, name="records"),
    path('report_pdf/', views.report_pdfView, name="report_pdf"),
    path('table/', views.tableView, name="table"),
    path('chart/', views.chartView, name="chart"),
    path('profile/', views.profileView, name="profile"),
    path('upload/', views.uploadView, name="upload"),
    path('logout/', views.logoutView, name="logout"),

]