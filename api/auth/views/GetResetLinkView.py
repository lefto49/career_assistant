from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage

from api.auth.NotAuthenticated import NotAuthenticated
from api.auth.serializers.PasswordResetSerializer import PasswordResetSerializer
from api.models import User


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
            mail_subject, message, from_email='medicine-organizer@yandex.ru', to=[request.data['email']]
        )
        email.send()

        return Response(status=status.HTTP_200_OK)