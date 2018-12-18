from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Q, Count
from django.http import Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serailizers import *

'''login page view'''


@csrf_exempt
def index(request):
    return render(request, 'login.html')


""" Home page after successful login"""

# def home(request):
#     data = request.user.userprofile
#     context = {
#         "data": data
#     }
#     return render(request, 'index.html', context)


''' post view '''


def postview(request):
    data = request.user.userprofile
    posts = CrimePost.objects.filter(user_profile=request.user.userprofile).order_by('-posted_on')
    current_loggedin_user = request.user
    followings = current_loggedin_user.userprofile.following.all().values_list('pk', flat=True)
    profiles = UserProfile.objects.filter(
        ~Q(following__pk__in=followings) & ~Q(user_id=current_loggedin_user.pk)
    )

    context = {
        "data": data,
        "posts": posts,
        'profiles': profiles
    }
    return render(request, 'index.html', context)


def action_post_view(request):
    comment = Comment.objects
    context = {
        'posts': CrimePost.objects.annotate(
            comment_count=Count('comment'), like_count=Count('like')
        ).filter(Q(comment_count__gt=4) | Q(like_count__gt=4)),
        'common_users': UserProfile.objects.filter(role=1)
    }
    return render(request, 'test.html', context)


''' post in home view'''


def post_In_home(request):
    data = request.user.userprofile
    common_post = CrimePost.objects.all().order_by('-posted_on')
    context = {
        "data": data,
        "common_post": common_post
    }
    return render(request, 'home.html', context)


def add_feed(request):
    current_loggedin_user = request.user
    followings = current_loggedin_user.userprofile.following.all().values_list('pk', flat=True)
    profiles = UserProfile.objects.filter(
        ~Q(following__pk__in=followings) & ~Q(user_id=current_loggedin_user.pk)
    )

    context = {
        'profiles': profiles
    }
    return render(request, 'test.html', context)


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
                return Response(data={'success': True, 'success_url': _user.userprofile.get_success_url})
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

    def get(self, request):
        userlist = UserProfile.objects.all().order_by('id')
        serialized_userlist = UserRegistrationSerializer(userlist, many=True)
        return Response(serialized_userlist.data)


class UserDetailsView(APIView):
    http_method_names = ['get', 'post', 'put', 'delete']

    def get(self, request, pk, format=None):
        userlist = UserProfile.objects.get(pk=pk)
        serialized_userlist = UserRegistrationSerializer(userlist, many=True)
        return Response(serialized_userlist.data)


class UserProfileApiView(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(UserProfileApiView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user = request.user.userprofile
        serialized_userlist = UserProfileSerializer(user)
        return Response(serialized_userlist.data)


''' CrimePostSerializer api view'''

import base64

from django.core.files.base import ContentFile


class CrimePostApiView(APIView):
    # parser_classes = (MultiPartParser, FormParser,)

    def get_object(self, pk):
        try:
            return CrimePost.objects.get(pk=pk)
        except CrimePost.DoesNotExist:
            raise Http404

    def post(self, request, *args, **kwargs):

        format, imgstr = request.data['images'].split(';base64,')
        ext = format.split('/')[-1]

        data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        _requested_data = request.data
        _requested_data['images'] = data

        serializer = CrimePostSerializer(data=_requested_data)
        if serializer.is_valid():
            serializer.save(user_profile=request.user.userprofile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        nypost = CrimePost.objects.all().order_by('-id')
        serializedData = CrimePostSerializer(nypost, many=True)
        return Response(serializedData.data)


class CommentApiView(APIView):
    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request):
        cmtlist = Comment.objects.all()
        serialized_cmtlist = CommentSerializer(cmtlist, many=True)
        return Response(serialized_cmtlist.data)

    def post(self, request, *args, **kwargs):
        _serializer = CommentSerializer(data=request.data)
        if _serializer.is_valid(raise_exception=True):
            _serializer.save(user=request.user)
            return Response(data=_serializer.data)
        return Response(data={'message': 'An error occured.'})


class ReplyApiView(APIView):
    def get_object(self, pk):
        try:
            return Reply.objects.get(pk=pk)
        except Reply.DoesNotExist:
            raise Http404

    def get(self, request):
        reply_list = Reply.objects.all()
        serialized_reply_list = ReplySerializer(reply_list, many=True)
        return Response(serialized_reply_list.data)

    def post(self, request, *args, **kwargs):
        _serializer = ReplySerializer(data=request.data)
        if _serializer.is_valid(raise_exception=True):
            _serializer.save(user=request.user)
            return Response(data=_serializer.data)
        return Response(data={'message': 'An error occured.'})


class LikeApiView(APIView):
    def get_object(self, pk):
        try:
            return Like.objects.get(pk=pk)
        except Like.DoesNotExist:
            raise Http404

    def get(self, request):
        total = Like.objects.all()
        serialized_like = LikeSerializer(total, many=True)
        return Response(serialized_like.data)

    def post(self, request, *args, **kwargs):
        _serializer = LikeSerializer(data=request.data)
        if _serializer.is_valid(raise_exception=True):
            try:
                _serializer.save(user=request.user)
                return Response(data=_serializer.data)
            except IntegrityError:
                _post = request.data.get('post')
                _likes = Like.objects.filter(post_id=_post, user=request.user).delete()
                return Response(data=_serializer.data)
            except Exception:
                return Response(data=_serializer.data)
        return Response(data={'message': 'An error occured.'})


class UserActiveDeactiveView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.data['user']
        user = UserProfile.objects.get(pk=user)
        dj_user = user.user
        dj_user.is_active = not dj_user.is_active
        dj_user.save()
        return Response(data={'success': True, 'is_active': dj_user.is_active})
