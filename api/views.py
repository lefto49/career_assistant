from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage

from .models import User
from .serializers import UserSerializer, LoginSerializer, PasswordResetSerializer, PasswordResetConfirmedSerializer
from .NotAuthenticated import NotAuthenticated


class CreateUserView(CreateAPIView, TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = RefreshToken.for_user(user)

        return Response({'user': serializer.data,
                         'refresh': str(token),
                         'access': str(token.access_token)}, status=status.HTTP_201_CREATED)


class LoginView(CreateAPIView, TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RetrieveUpdateUserView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.data.get('id', 1))
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = User.objects.get(id=request.data.get('id', 1))
        serializer = self.serializer_class(user, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordResetView(CreateAPIView):
    permission_classes = (NotAuthenticated,)
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '')

        if not User.objects.filter(email=email).exists():
            return Response({'error': 'user with such email does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(email=email)
        token = PasswordResetTokenGenerator().make_token(user)
        id = urlsafe_base64_encode(str(user.id).encode('utf-8'))
        domain = get_current_site(request=request).domain
        reset_path = 'http://' + domain + '/' + id + '/' + token

        mail_subject = 'Password Reset'
        message = "Hello from Career Assistant! \nRecently you've asked to reset your password." \
                  " Click on the following link for further instructions: \n{0}\n" \
                  "If you didn't ask to reset your password, just ignore this email.".format(reset_path)
        email = EmailMessage(
            mail_subject, message, from_email='careerassistant@yandex.ru',  to=[email]
        )
        email.send()

        return Response(status=status.HTTP_200_OK)


class ValidateResetPasswordView(CreateAPIView):
    permission_classes = (NotAuthenticated,)
    serializer_class = PasswordResetConfirmedSerializer

    def post(self, request, *args, **kwargs):
        id = int(urlsafe_base64_decode(request.data.get('id', '')).decode('utf-8'))

        if not User.objects.filter(id=id).exists():
            return Response({'error': 'user with such an id does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=id)

        if not PasswordResetTokenGenerator().check_token(user, request.data.get('token', '')):
            return Response({'error': 'invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(request.data.get('password', ''))
        user.save()

        return Response(status=status.HTTP_200_OK)
