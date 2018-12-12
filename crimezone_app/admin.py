from django.contrib import admin
from .models import UserProfile,CrimePost,Comment,Reply,Like
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(CrimePost)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Like)