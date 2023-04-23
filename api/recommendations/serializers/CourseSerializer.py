from rest_framework import serializers

from api.data.Course import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'description', 'link']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in ('title', 'description', 'link'):
            if not data[field]:
                data[field] = ''
        return data
