from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode

from rest_framework import serializers

from rest_framework_simplejwt.exceptions import InvalidToken
from django.core.exceptions import ObjectDoesNotExist

from api.models import User


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
