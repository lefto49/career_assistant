from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from django.core.mail import EmailMessage

from api.auth.utils import generate_code
from api.data.Confirmation import Confirmation
from api.models import User


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
            mail_subject, message, from_email='medicine-organizer@yandex.ru', to=[email]
        )
        email.send()
        return Response(status=status.HTTP_200_OK)
