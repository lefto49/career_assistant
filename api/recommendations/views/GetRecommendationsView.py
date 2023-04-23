from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.recommendations.serializers.CourseSerializer import CourseSerializer
from api.recommendations.serializers.CupSerializer import CupSerializer
from api.recommendations.serializers.VacancySerializer import VacancySerializer
from api.recommendations.utils import get_user_from_token


class GetRecommendationsView(RetrieveAPIView):
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

        vacancies = []
        for vacancy in user.vacancies.all():
            vacancies.append(VacancySerializer(vacancy).data)

        cups = []
        for cup in user.cups.all():
            cups.append(CupSerializer(cup).data)

        courses = []
        for course in user.courses.all():
            courses.append(CourseSerializer(course).data)

        return Response({'vacancies': vacancies, 'cups': cups, 'courses': courses}, status=status.HTTP_200_OK)
