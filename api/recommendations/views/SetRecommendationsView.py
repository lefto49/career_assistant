from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.data.Course import Course
from api.data.Cup import Cup
from api.data.Vacancy import Vacancy
from api.recommendations.RecomendSystem import getRecomendation
from api.recommendations.utils import get_user_from_token


class SetRecommendationsView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """
        Returns the recommendations for a user
        :param request: data that must be passed: access token.
        :return: 400 status code if a user with such an id does not exist,
        200 and list of recommendations if everything is ok
        """
        try:
            user = get_user_from_token(request.headers['Authorization'])
        except ObjectDoesNotExist:
            return Response({'error': 'User with such an id does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        user.vacancies.clear()
        user.cups.clear()
        user.courses.clear()

        vacancies = getRecomendation(user.experience, 10, 'vacancy')
        for vac_id in vacancies['id']:
            if Vacancy.objects.filter(id=vac_id).exists():
                user.vacancies.add(Vacancy.objects.get(id=vac_id))

        cups = getRecomendation(user.experience, 5, 'cup')
        for cup_id in cups['id']:
            if Cup.objects.filter(id=cup_id).exists():
                user.cups.add(Cup.objects.get(id=cup_id))

        course = getRecomendation(user.experience, 3, 'course')
        for course_id in course['id']:
            if Course.objects.filter(id=course_id).exists():
                user.courses.add(Course.objects.get(id=course_id))

        user.save()
