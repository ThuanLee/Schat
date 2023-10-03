from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Friend, Notification
from drf_spectacular.utils import extend_schema_serializer
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password, check_password

class UserSerializer(serializers.ModelSerializer):
    username=serializers.CharField(required=False)
    password=serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
    
    def validate(self, data):
        if self.instance is not None:
            return data
        if any(field not in data for field in ['username', 'email', 'password']):
            raise serializers.ValidationError('Username, email and password must be provided')
        return data

    def validate_username(self, value):
        if len(value) < 3:
            raise serializers.ValidationError('Username must be at least 3 characters')
        elif ' ' in value:
            raise serializers.ValidationError('Username must not contain a blank')
        return value
    
    def validate_password(self, value):
        if len(value) < 7:
            raise serializers.ValidationError('Password must be at least 7 characters')
        elif ' ' in value:
            raise serializers.ValidationError('Password must not contain a blank')
        return make_password(value)
    
    def validate_email(self, value):
        if ' ' in value:
            raise serializers.ValidationError('Email must not contain a blank')
        return value
    
    def get(self):
        data = self.data
        return {
            'username': data['username'],
            'email': data['email']
        }

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class FriendSerializer(serializers.ModelSerializer):
    friend_with = serializers.SerializerMethodField()

    def get_friend_with(self, obj):
        friendProfile = UserProfile.objects.get(user=obj.friend_with)
        friendProfileSerializer = UserProfileSerializer(friendProfile, many=False)
        friendSerializer = UserSerializer(obj.friend_with, many=False)
        return friendSerializer.get() | friendProfileSerializer.data
    
    class Meta:
        model = Friend
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'