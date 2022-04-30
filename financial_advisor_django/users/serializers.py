from django.contrib.auth.models import User
from .models import UserProfile
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'groups']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'name', 'interests',
                  'hobbies', 'age', 'gender', 'net_worth']
