from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


class RegisterSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
    def save(self, **kwargs):
        email = self.validated_data['email']
        username = self.validated_data['username']
        password = self.validated_data['password']
        
        user = User(
            email=email,
            username=username
        )
        
        user.set_password(password)
        user.save()
        return user
        
        
class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(username=obj['username'])

        return {
            'access': user.token()['access'],
            'refresh': user.token()['refresh'],
        }

    class Meta:
        model = User
        fields = ['username', 'password', 'tokens']

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')

        user = auth.authenticate(username=username, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again.')
        
        return {
            'username': user.username,
            'tokens': user.token()
        }