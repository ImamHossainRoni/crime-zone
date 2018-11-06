from rest_framework import serializers
from .models import UserProfile
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import transaction

''' Serializer for user registration'''
class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('username', 'first_name', 'last_name',)

    def is_valid(self, raise_exception=True):
        if self.initial_data.get('password') != self.initial_data.get('confirm_password'):
            raise ValidationError({'message': 'Password and Confirm Password doesn\'t match'})
        return super(UserRegistrationSerializer, self).is_valid(raise_exception=raise_exception)

    def create(self, attrs):
        with transaction.atomic():
            _user = User(
                username=self.initial_data.get('username'),
                first_name=self.initial_data.get('first_name'),
                last_name=self.initial_data.get('last_name')
            )
            _user.set_password(self.initial_data.get('password'))
            _user.save()
            _profile = UserProfile(user_id=_user.pk)
            _profile.save()
            return _profile

    def get_username(self, obj):
        return obj.user.username if obj.user else None

    def get_first_name(self, obj):
        return obj.user.first_name if obj.user else None

    def get_last_name(self, obj):
        return obj.user.last_name if obj.user else None


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        fields = ('username', 'password',)
