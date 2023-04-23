from rest_framework import serializers

from api.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'last_name', 'first_name', 'birth_year', 'city',
                  'university', 'vacancy', 'experience', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if 'birth_year' in data.keys():
            if data['birth_year'] < 1920 or data['birth_year'] > 2021:
                raise serializers.ValidationError({'birth_year': 'the value must be between 1920 and 2021'})

        return data

    def update(self, instance, validated_data):
        super().update(instance, validated_data)

        if 'password' in validated_data.keys():
            instance.set_password(validated_data['password'])
            instance.save()

        return instance
