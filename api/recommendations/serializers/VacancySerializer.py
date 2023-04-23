from rest_framework import serializers

from api.data.Vacancy import Vacancy


class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = ['title', 'description']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in ('title', 'description'):
            if not data[field]:
                data[field] = ''
        return data
