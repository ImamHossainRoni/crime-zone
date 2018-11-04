from django.urls import path
from .views import *


urlpatterns = [
    path('create-user/', UserRegistrationView.as_view()),
]