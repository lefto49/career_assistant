from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from api.auth.NotAuthenticated import NotAuthenticated
from api.auth.serializers.UserSerializer import UserSerializer
import requests


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

        url = 'http://127.0.0.1:8000/api/scoring/set/'
        headers = {'Authorization': "Bearer " + str(token.access_token)}
        r = requests.get(url, headers=headers)
        user.scoring_value = float(r.json()['scoring_result'])
        user.save()

        url = 'http://127.0.0.1:8000/api/recommendations/set/'
        requests.get(url, headers=headers)

        return Response({'user': serializer.data,
                         'refresh': str(token),
                         'access': str(token.access_token)}, status=status.HTTP_201_CREATED)