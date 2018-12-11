from django.urls import path,include
from . import views
from .views import *

urlpatterns = [
    path('api/create-user/', UserRegistrationView.as_view()),
    path('api/login/', LoginApiView.as_view()),
    path('api/logout/', LogoutView.as_view()),
    path('api/user/', UserProfileApiView.as_view()),
    path('', views.index,name="index-view"),
    path('signout/', views.LogoutView.as_view()),
    path('api/post/', CrimePostApiView.as_view()),
    path('post/', views.postview,name="post-view"),
    path('commonpost/', views.post_In_home,name="post-in-home-view"),
    path('test/', views.add_feed,name="following_user"),
    path('comment/', CommentApiView.as_view()),

]
