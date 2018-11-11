from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from .serailizers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from rest_framework.response import Response
from rest_framework import generics, status
from django.shortcuts import render,HttpResponse, redirect
from django.core.exceptions import ObjectDoesNotExist
from  django.http import Http404
from .models import UserProfile
from django.contrib.auth import authenticate, login,logout

'''login page view'''
@csrf_exempt
def index(request):
    return render(request,'login.html')
""" Home page after successful login"""
def home(request):
    data = request.user.userprofile
    context = {
        "data": data
    }
    return render(request,'index.html',context)


'''Login api view'''
class LoginApiView(APIView):
    def post(self, request, *args, **kwargs):
        _serializer = UserLoginSerializer(data=request.data)
        if _serializer.is_valid(raise_exception=True):
            _user = authenticate(
                username=_serializer.data['username'], 
                password=_serializer.data['password']
            )
            if _user is not None:
                login(request, _user)
                return Response(data={'success': True})
        return Response(data={'success': False})

'''Logout api view'''
class LogoutView(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LogoutView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response_data = {
            "status": status.HTTP_204_NO_CONTENT,
            "message": "Successfully logout."
        }
        try:
            request.session.flush()
            return Response(data=response_data)
        except (AttributeError, ObjectDoesNotExist):
            response_data['status'] = status.HTTP_400_BAD_REQUEST
            response_data['message'] = "Failed to logout. Please contact."
            return Response(data=response_data)

'''User registration api view'''
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

class UserDetailsView(APIView):
    http_method_names = ['get', 'post', 'put', 'delete']

    def get(self,request,pk,format=None):
        userlist = UserProfile.objects.get(pk=pk)
        serialized_userlist = UserRegistrationSerializer(userlist,many = True)
        return Response(serialized_userlist.data)

class UserProfileApiView(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(UserProfileApiView, self).dispatch(request, *args, **kwargs)

    def get(self,request, *args, **kwargs):
        user = request.user.userprofile
        serialized_userlist =UserProfileSerializer(user)
        return Response(serialized_userlist.data)
