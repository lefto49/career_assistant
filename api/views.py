from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import check_password

from .models import User
from .serializers import UserSerializer


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


class LoginView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email=request.data['email'])
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not check_password(request.data['password'], user.password):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken.for_user(user)
        return Response({'user': self.serializer_class(user).data,
                         'refresh': str(token),
                         'access': str(token.access_token)}, status=status.HTTP_200_OK)


class RetrieveUpdateUserView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        pass
