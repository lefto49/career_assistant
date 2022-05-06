from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage

from .models import User, Confirmation
from .serializers import UserSerializer, LoginSerializer, PasswordResetSerializer, VacancySerializer, CupSerializer, \
    CourseSerializer
from .NotAuthenticated import NotAuthenticated
from .utils import generate_code, set_recommendations, get_user_from_token, get_scoring_verdict
from .ScoringSystem import process_users


class CreateUserView(CreateAPIView, TokenObtainPairView):
    permission_classes = (NotAuthenticated,)
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
        user.scoring_value = process_users(user.experience, user.vacancy)
        set_recommendations(user)
        user.save()

        return Response({'user': serializer.data,
                         'refresh': str(token),
                         'access': str(token.access_token)}, status=status.HTTP_201_CREATED)


class LoginView(CreateAPIView, TokenObtainPairView):
    permission_classes = (NotAuthenticated,)
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
        try:
            user = get_user_from_token(request.headers['Authorization'])
        except ObjectDoesNotExist:
            return Response({'error': 'User with such an id does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        """
        Updates user data.
        Returns 400 status if new data was incorrect.
        :param request: data that must be passed: User model fields that were changed.
        :return: refreshed user data.
        """
        try:
            user = get_user_from_token(request.headers['Authorization'])
        except ObjectDoesNotExist:
            return Response({'error': 'User with such an id does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(user, data=request.data, partial=True)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        user.scoring_value = process_users(user.experience, user.vacancy)
        set_recommendations(user)
        user.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetResetLinkView(CreateAPIView):
    permission_classes = (NotAuthenticated,)
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        """
        Sends an email that allows the user to reset the password.
        Returns 400 status if user with such an email does not exist.
        :param request: data that must be passed: user's email.
        """
        if not User.objects.filter(email=request.data['email']).exists():
            return Response({'error': 'User with such email does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(email=request.data['email'])
        # Creates all the necessary parts for a reset link.
        token = PasswordResetTokenGenerator().make_token(user)
        encoded_uid = urlsafe_base64_encode(str(user.id).encode('utf-8'))
        # domain = get_current_site(request=request).domain
        reset_path = 'http://localhost:3000/forgotPassword?' + 'encodeUid=' + encoded_uid + '&' + 'token=' + token

        mail_subject = 'Password Reset'
        message = "Hello from Career Assistant! \n\nRecently you've asked to reset your password." \
                  " Click on the following link for further instructions: \n{0}\n\n" \
                  "If you didn't ask to reset your password, just ignore this email.".format(reset_path)
        email = EmailMessage(
            mail_subject, message, from_email='careerassistant@yandex.ru', to=[request.data['email']]
        )
        email.send()

        return Response(status=status.HTTP_200_OK)


class PasswordResetView(CreateAPIView):
    permission_classes = (NotAuthenticated,)
    serializer_class = PasswordResetSerializer

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
            return Response({'error': 'User with such an id does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidToken:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=serializer.data['id'])
        user.set_password(serializer.data['password'])
        user.save()

        return Response(status=status.HTTP_200_OK)


class GetConfirmationCodeView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        """
        Sends an email with a confirmation code to the user that wants to sign up.
        :param request: data that must be passed: user's email address.
        :return: 400 status code if a user with such an email already exists, 200 if everything is ok
        """
        code = generate_code()
        email = request.data['email']

        if User.objects.filter(email=email).exists():
            return Response({'error': 'User with such an email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        if Confirmation.objects.filter(email=email).exists():
            confirmation = Confirmation.objects.get(email=email)
            confirmation.code = code
        else:
            confirmation = Confirmation(code=code, email=email)

        confirmation.save()

        mail_subject = 'Email Confirmation'
        message = "Hello from Career Assistant! \n\nEnter this code to confirm your email:\n{0}".format(code)
        email = EmailMessage(
            mail_subject, message, from_email='careerassistant@yandex.ru', to=[email]
        )
        email.send()
        return Response(status=status.HTTP_200_OK)


class ConfirmEmailView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        """
        Checks if entered confirmation code equals the one that was sent.
        :param request: data that must be passed: email, entered code.
        :return: 400 status code if a confirmation code was not sent to such an email or incorrect code was entered,
        200 if everything is ok
        """
        email = request.data['email']
        code = request.data['code']

        if not Confirmation.objects.filter(email=email).exists():
            return Response({'error': 'No confirmation code was sent to this email'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not Confirmation.objects.filter(email=email, code=code).exists():
            return Response({'error': 'Incorrect confirmation code'}, status=status.HTTP_400_BAD_REQUEST)

        confirmation = Confirmation.objects.get(email=email, code=code)
        confirmation.delete()

        return Response({'email': email}, status=status.HTTP_200_OK)


class GetRecommendationsView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """
        Returns the recommendations for a user
        :param request: data that must be passed: access token.
        :return: 400 status code if a user with such an id does not exist,
        200 and list of recommendations if everything is ok
        """
        try:
            user = get_user_from_token(request.headers['Authorization'])
        except ObjectDoesNotExist:
            return Response({'error': 'User with such an id does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        vacancies = []
        for vacancy in user.vacancies.all():
            vacancies.append(VacancySerializer(vacancy).data)

        cups = []
        for cup in user.cups.all():
            cups.append(CupSerializer(cup).data)

        courses = []
        for course in user.courses.all():
            courses.append(CourseSerializer(course).data)

        return Response({'vacancies': vacancies, 'cups': cups, 'courses': courses}, status=status.HTTP_200_OK)


class ScoringResultView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """
        Returns the scoring result string interpretation.
        :param request: data that must be passed: access token.
        :return: 400 status code if a user with such an id does not exist,
        200 and list of recommendations if everything is ok
        """
        try:
            user = get_user_from_token(request.headers['Authorization'])
        except ObjectDoesNotExist:
            return Response({'error': 'User with such an id does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'verdict': get_scoring_verdict(user.scoring_value)}, status=status.HTTP_200_OK)
