from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from jwt import decode
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage

import career_assistant.settings

from .models import User
from .serializers import UserSerializer, LoginSerializer, PasswordResetSerializer, PasswordResetConfirmedSerializer
from .NotAuthenticated import NotAuthenticated


class CreateUserView(CreateAPIView, TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        """
        Manages the process of creating a new user.
        Returns 400 status if incorrect data was passed.
        :param request: data that must be passed: lastname, firstname, birth year, city,
                                                  university, vacancy, experience, email, password.
        :return: user data, access and refresh tokens.
        """
        serializer = self.serializer_class(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()

        token = RefreshToken.for_user(user)

        return Response({'user': serializer.data,
                         'refresh': str(token),
                         'access': str(token.access_token)}, status=status.HTTP_201_CREATED)


class LoginView(CreateAPIView, TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Manages the process of logging in a user.
        Returns 401 status if incorrect user credentials were passed.
        :param request: data that must be passed: email, password.
        :return: user data, access and refresh tokens.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RetrieveUpdateUserView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        """
        Gets user information using id decoded from an access token.
        Returns 400 status if user with such an id does not exist.
        :return: data of the user with the specified id.
        """
        token = request.headers['Authorization'][7:]
        uid = decode(token, career_assistant.settings.SECRET_KEY, algorithms=['HS256'])['user_id']

        if not User.objects.filter(id=uid).exists():
            return Response({'error': 'user with such an id does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=uid)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        """
        Updates user data.
        Returns 400 status if new data was incorrect.
        :param request: data that must be passed: all User model fields including both changed and unchanged.
        :return: refreshed user data.
        """
        user = User.objects.get(id=request.data.get('id', 1))
        serializer = self.serializer_class(user, data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordResetView(CreateAPIView):
    permission_classes = (NotAuthenticated,)
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        """
        Sends an email that allows the user to reset the password.
        Returns 400 status if user with such an email does not exist.
        :param request: data that must be passed: user's email.
        """
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ObjectDoesNotExist:
            return Response({'error': 'user with such email does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(email=serializer.data['email'])
        # Creates all the necessary parts for a reset link.
        token = PasswordResetTokenGenerator().make_token(user)
        encoded_uid = urlsafe_base64_encode(str(user.id).encode('utf-8'))
        domain = get_current_site(request=request).domain
        reset_path = 'https://' + domain + '/' + encoded_uid + '/' + token

        mail_subject = 'Password Reset'
        message = "Hello from Career Assistant! \nRecently you've asked to reset your password." \
                  " Click on the following link for further instructions: \n{0}\n" \
                  "If you didn't ask to reset your password, just ignore this email.".format(reset_path)
        email = EmailMessage(
            mail_subject, message, from_email='careerassistant@yandex.ru', to=[serializer.data['email']]
        )
        email.send()

        return Response(status=status.HTTP_200_OK)


class ValidateResetPasswordView(CreateAPIView):
    permission_classes = (NotAuthenticated,)
    serializer_class = PasswordResetConfirmedSerializer

    def post(self, request, *args, **kwargs):
        """
        Updates the user's password in the database.
        Returns 400 status if user with such an id does not exist or an invalid token was passed.
        :param request: data that must be passed: encoded user id, reset token, new password.
        """
        serializer = self.serializer_class(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ObjectDoesNotExist:
            return Response({'error': 'user with such an id does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidToken:
            return Response({'error': 'invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=serializer.data['id'])
        user.set_password(serializer.data['password'])
        user.save()

        return Response(status=status.HTTP_200_OK)
