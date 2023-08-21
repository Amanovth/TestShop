from rest_framework import generics, status
from rest_framework.response import Response
from .models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from random import randint
from .serializers import *
from src.base.utils import Util


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            email = serializer.data['email']
            user = User.objects.get(email=email)
            user.code = randint(100_000, 999_999)
            user.save()
            
            email_body = f"To confirm registration in the system, enter the code below:\n\n" \
                         f"{user.code}"
            
            email_data = {
                'email_body': email_body,
                'email_subject': 'Подтвердите свою регистрацию',
                'to_email': user.email
            }
            
            Util.send_email(email_data)
            
            return Response({
                'message': 'User registered successfully. Code was send to the email.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    
    
class VerifyEmailAPIView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        code = serializer.data['code']
        email = serializer.data['email']

        try:
            user = User.objects.get(email=email)

            if user.is_verified:
                return Response({'message': _('Account is already verified')})
            if user.code == code:
                user.is_verified = True
                user.code = None
                user.save()
                return Response({'message': _('Activation was successful!')})
            return Response({'message': _('Wrong code entered')})
        except ObjectDoesNotExist:
            return Response({'message': _('User with this email does not exist')})


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)