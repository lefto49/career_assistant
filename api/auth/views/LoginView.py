from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView

from api.auth.NotAuthenticated import NotAuthenticated
from api.auth.serializers.LoginSerializer import LoginSerializer


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
