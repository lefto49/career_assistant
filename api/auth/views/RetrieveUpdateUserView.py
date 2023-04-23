from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.auth.serializers.UserSerializer import UserSerializer
import requests

from api.auth.utils import get_user_from_token


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

        url = 'http://127.0.0.1:8000/api/scoring/set/'
        headers = {'Authorization': request.headers['Authorization']}
        r = requests.get(url, headers=headers)
        user.scoring_value = float(r.json()['scoring_result'])
        user.save()

        url = 'http://127.0.0.1:8000/api/recommendations/set/'
        requests.get(url, headers=headers)

        return Response(serializer.data, status=status.HTTP_200_OK)
