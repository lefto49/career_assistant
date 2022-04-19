from django.contrib.auth.models import update_last_login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode

from rest_framework import serializers

from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from django.core.exceptions import ObjectDoesNotExist

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'last_name', 'first_name', 'birth_year', 'city',
                  'university', 'vacancy', 'experience', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        super().update(instance, validated_data)

        if 'password' in validated_data.keys():
            instance.set_password(validated_data['password'])
            instance.save()

        return instance


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['user'] = UserSerializer(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=37)
    id = serializers.CharField(max_length=37)
    token = serializers.CharField(max_length=1024)

    def validate(self, data):
        try:
            decoded_uid = int(urlsafe_base64_decode(data['id']).decode('utf-8'))
        except:
            raise ObjectDoesNotExist

        data['id'] = decoded_uid

        if not User.objects.filter(id=decoded_uid).exists():
            raise ObjectDoesNotExist

        user = User.objects.get(id=decoded_uid)
        if not PasswordResetTokenGenerator().check_token(user, data['token']):
            raise InvalidToken

        return data
