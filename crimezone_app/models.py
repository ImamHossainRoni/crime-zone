from crequest.middleware import CrequestMiddleware
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

ROLE_CHOICES = (
    (1, 'Common User'),
    (2, 'Action Applier'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.IntegerField(choices=ROLE_CHOICES, null=True)
    followers = models.ManyToManyField('UserProfile',
                                       related_name='followers_profile',
                                       blank=True)
    following = models.ManyToManyField('UserProfile',
                                       related_query_name='following_profile',
                                       blank=True)
    profile_pic = models.ImageField(upload_to='profile_image', null=True, blank=True)
    joining_time = models.DateTimeField(auto_now_add=True, auto_now=False)

    @property
    def get_username(self):
        return self.user.first_name + ' ' + self.user.last_name if self.user else None

    @property
    def name(self):
        try:
            return "{0} {1}".format(self.user.first_name, self.user.last_name)
        except Exception:
            return self.user.username

    def get_number_of_followers(self):
        print(self.followers.count())
        if self.followers.count():
            return self.followers.count()
        else:
            return 0

    def get_number_of_following(self):
        print(self.following.count())
        if self.following.count():
            return self.following.count()
        else:
            return 0

    @property
    def get_success_url(self):
        if self.role == ROLE_CHOICES[0][0]:
            return '/post/'
        return '/action-posts/'

    def __str__(self):
        return self.get_username


class CrimePost(models.Model):
    user_profile = models.ForeignKey(UserProfile,
                                     on_delete=models.PROTECT, null=True, blank=True)
    title = models.TextField()
    images = models.ImageField(upload_to='post_images', null=True, blank=True)
    posted_on = models.DateTimeField(auto_now_add=True, auto_now=False)

    def get_number_of_likes(self):
        return self.like_set.count()

    def get_number_of_comments(self):
        return self.comment_set.count()

    @property
    def is_liked_by_me(self):
        status = False
        try:
            request = CrequestMiddleware.get_request()
            user = request.user
            if self.like_set.filter(user_id=user.id).exists():
                status = True
        except Exception:
            pass
        return status

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('CrimePost', on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    comment = models.CharField(max_length=100)
    commented_on = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.comment


class Reply(models.Model):
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.CharField(max_length=100)
    replied_on = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.reply


class Like(models.Model):
    post = models.ForeignKey('CrimePost', on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return 'Like: ' + self.user.username + '' + self.post.title
