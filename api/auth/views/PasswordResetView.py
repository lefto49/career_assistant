from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from rest_framework_simplejwt.exceptions import InvalidToken

from api.auth.NotAuthenticated import NotAuthenticated
from api.auth.serializers.PasswordResetSerializer import PasswordResetSerializer
from api.models import User


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
