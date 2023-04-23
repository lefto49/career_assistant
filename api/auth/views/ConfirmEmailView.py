from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from api.data.Confirmation import Confirmation


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
