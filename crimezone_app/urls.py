from django.urls import path,include
from . import views
from .views import *
#App Url

urlpatterns = [
    path('api/create-user/', UserRegistrationView.as_view()),
    path('api/login/', LoginApiView.as_view()),
    path('api/logout/', LogoutView.as_view()),
    path('api/user/<int:pk>/', UserProfileApiView.as_view()),
    path('', views.index,name="index-view"),
]
