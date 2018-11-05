from django.urls import path,include
from . import views
from .views import *
#App Url

urlpatterns = [
    path('create-user/', UserRegistrationView.as_view()),
    #path('user/<int:pk>/', UserDetailsView.as_view()),
    path('', views.registration,name="reg"),
    path('login/', views.login_user,name="login"),
    path('home/', views.home,name="home"),
   
   


]