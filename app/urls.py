from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeView, name="home"),
    path('profile/', views.profileView, name="profile"),
    path('dashboard/', views.dashboardView, name="dashboard"),
    path('log_Reg/', views.loginRegisterView, name="logReg"),
    path('logout/', views.logoutView, name="logout"),

]