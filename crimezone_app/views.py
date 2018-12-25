from datetime import datetime

from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Q, Count
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from crimezone_app.helpers import send_email_to_users
from .serailizers import *

# def pageloder(request):
#     comment = Comment.objects
#     context = {
#         'posts': CrimePost.objects.annotate(
#             comment_count=Count('comment'), like_count=Count('like')
#         ).filter(Q(comment_count__gt=4) | Q(like_count__gt=4)),
#         'common_users': UserProfile.objects.filter(role=1)
#     }
#     return render(request, 'action.html', context)
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



def search(request):
    value = request.GET.get('query')
    data = CrimePost.objects.filter(Q(title__icontains=value) | Q(title__icontains=value))
    return render(request, '', context={'data': data})


''' post view '''


def postview(request):
    data = request.user.userprofile
    posts = CrimePost.objects.filter(user_profile=request.user.userprofile).order_by('-posted_on')
    current_loggedin_user = request.user
    followings = current_loggedin_user.userprofile.following.all().values_list('pk', flat=True)
    profiles = UserProfile.objects.filter(
        ~Q(following__pk__in=followings) & ~Q(user_id=current_loggedin_user.pk)
    )
    post_of_the_day = CrimePost.objects.filter(

        posted_on__gte=datetime.now().replace(hour=0, minute=0, second=0),
        posted_on__lte=datetime.now().replace(hour=23, minute=59, second=59)
    ).annotate(like_count=Count('like')).filter(like_count__gt=0).order_by('like_count').first()

    # top_5_post = CrimePost.objects.filter()
    context = {
        "data": data,
        "posts": posts,
        'profiles': profiles,
        'post_of_the_day': post_of_the_day
    }
    return render(request, 'index.html', context)


# user post
def userpost(request, id):
    _user = get_object_or_404(UserProfile, pk=id)
    posts = CrimePost.objects.filter(user_profile=_user).order_by('-posted_on')
    post_of_the_day = CrimePost.objects.filter(

        posted_on__gte=datetime.now().replace(hour=0, minute=0, second=0),
        posted_on__lte=datetime.now().replace(hour=23, minute=59, second=59)
    ).annotate(like_count=Count('like')).filter(like_count__gt=0).order_by('like_count').first()

    context = {
        "data": _user,
        "posts": posts,
        'post_of_the_day': post_of_the_day
    }
    return render(request, 'userpost.html', context)


def action_post_view(request):
    data = request.user.userprofile
    comment = Comment.objects
    context = {
        "data": data,
        'posts': CrimePost.objects.annotate(
            comment_count=Count('comment'), like_count=Count('like')
        ).filter(Q(comment_count__gt=1) | Q(like_count__gt=1)),
        'common_users': UserProfile.objects.filter(role=1)
    }
    return render(request, 'action.html', context)


''' post in home view'''


def post_In_home(request):
    data = request.user.userprofile
    common_post = CrimePost.objects.all().order_by('-posted_on')
    current_loggedin_user = request.user
    followings = current_loggedin_user.userprofile.following.all().values_list('pk', flat=True)
    profiles = UserProfile.objects.filter(
        ~Q(following__pk__in=followings) & ~Q(user_id=current_loggedin_user.pk)
    )

    context = {
        "data": data,
        "common_post": common_post,
        'profiles': profiles
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


def report_view(request):
    userinfo = request.user.userprofile
    queryset = CrimePost.objects.aggregate(
        total_active_users=Count('user_profile_id', distinct=True),
        total_commented_users=Count('comment__user_id', distinct=True),
        total_replied_users=Count('comment__reply__user_id', distinct=True),
        total_liked_users=Count('like__user_id', distinct=True),

    )
    total_system_users = UserProfile.objects.count()

    return render(request, 'report.html', {'data': queryset, 'total_users': total_system_users, 'userinfo': userinfo})


def crime_view(request):
    data = request.user.userprofile
    comment = Comment.objects
    context = {
        "data": data,
        'posts': CrimePost.objects.annotate(
            comment_count=Count('comment'), like_count=Count('like')
        ).filter(Q(comment_count__gt=1) | Q(like_count__gt=1)),
        'common_users': UserProfile.objects.filter(role=1)
    }
    return render(request, 'crime.html', context)


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
        try:
            format, imgstr = request.data['images'].split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            _requested_data = request.data
            _requested_data['images'] = data
        except Exception as exp:
            _requested_data = request.data
            _requested_data.pop('images', None)

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
                _like = _serializer.save(user=request.user)
                _data = dict(_serializer.data)
                _data.update({'total_likes': _like.post.total_likes})
                return Response(data=_data)
            except IntegrityError:
                _post = request.data.get('post')
                _likes = Like.objects.filter(post_id=_post, user=request.user).delete()
                _data = dict(_serializer.data)
                _data.update({'total_likes': CrimePost.objects.get(pk=_post).total_likes})
                return Response(data=_data)
            except Exception as exp:
                return Response(data=_serializer.data)
        return Response(data={'message': 'An error occured.'})


class UserActiveDeactiveView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.data['user']
        user = UserProfile.objects.get(pk=user)
        dj_user = user.user
        dj_user.is_active = not dj_user.is_active
        dj_user.save()
        # send_email_to_users(emails=[dj_user.username], body='Test', subject='YES')

        active_msg = 'Now you are permitted to access your account.'
        deactive_msg = 'Now you are not permitted to access your account.'
        if dj_user.is_active:
            send_email_to_users(emails=[dj_user.username], body=active_msg, subject='CrimeZone Access Control')
        else:
            send_email_to_users(emails=[dj_user.username], body=deactive_msg, subject='CrimeZone Access Control')
        return Response(data={'success': True, 'is_active': dj_user.is_active})


''' SearchAPiView'''


class SearchAPiView(APIView):
    def get_object(self, pk):
        try:
            return CrimePost.objects.get(pk=pk)
        except CrimePost.DoesNotExist:
            raise Http404

    def get(self, request):
        cmtlist = CrimePost.objects.all()
        serialized_cmtlist = CrimePostSearchSerializer(cmtlist, many=True)
        return Response(serialized_cmtlist.data)
