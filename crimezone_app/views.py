from rest_framework.views import APIView
from .serailizers import UserRegistrationSerializer
from rest_framework.response import Response
from django.shortcuts import render,HttpResponse, redirect
from  django.http import Http404
from .models import UserProfile

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