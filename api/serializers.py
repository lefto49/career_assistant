from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        # if api_settings.UPDATE_LAST_LOGIN:
        #     update_last_login(None, self.user)

        return data
