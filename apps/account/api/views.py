from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer, ResetPasswordSerializer, \
    SetNewPasswordSerializer, ChangeNewPasswordSerializer, AccountSerializer
from rest_framework import generics, views, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from drf_yasg import openapi
from apps.account.models import Account
from apps.account.api.utils import Util
import jwt


class AccountRegisterAPIView(generics.GenericAPIView):
    # http://127.0.0.1:8000/account/register/
    serializer_class = RegisterSerializer

    # user create
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # user details or data
        user_data = serializer.data
        user = Account.objects.get(email=user_data['email'])

        # get refresh token
        token = RefreshToken.for_user(user)

        # activate account with email
        current_site = '127.0.0.1:8000/'
        relative_link = 'account/verify-email/'
        abs_url = f'http://{current_site}{relative_link}?token={str(token.access_token)}'
        email_body = f'Hi, {user.email} \n User link below to activate your email \n {abs_url}'
        data = {
            'to_email': user.email,
            'email_subject': 'Activate email to Eski Toshmi MedTexnika',
            'email_body': email_body
        }
        Util.send_email(data)

        return Response({'success': True, 'message': 'Activate url was sent your email'},
                        status=status.HTTP_201_CREATED)
