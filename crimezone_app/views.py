from rest_framework.views import APIView
from .serailizers import UserRegistrationSerializer
from rest_framework.response import Response
from django.shortcuts import render,HttpResponse, redirect
from  django.http import Http404
from .models import UserProfile
from django.contrib.auth import authenticate, login, logout

def registration(request):
    return render(request,'login.html')
    
def home(request):
    return render(request,'home.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            print("Not matched")
    return render(request, 'home.html')

class UserRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        _serializer = UserRegistrationSerializer(data=request.data)
        if _serializer.is_valid(raise_exception=True):
            _serializer.save()
            return Response(data=_serializer.data)
        return Response(data={'message': 'An error occured.'})

    def get(self,request):
        userlist = UserProfile.objects.all().order_by('id')
        serialized_userlist = UserRegistrationSerializer(userlist,many = True)
        return Response(serialized_userlist.data)

# class UserDetailsView(APIView):
#     http_method_names = ['get', 'post', 'put', 'delete']

#     def get(self,request,pk,format=None):
#         userlist = UserProfile.objects.all(pk)
#         serialized_userlist = UserRegistrationSerializer(userlist,many = True)
#         return Response(serialized_userlist.data)

