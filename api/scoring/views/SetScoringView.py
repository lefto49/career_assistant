from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.scoring.ScoringSystem import process_users
from api.scoring.utils import get_user_from_token, get_scoring_verdict


class SetScoringView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """
        Returns the scoring result string interpretation.
        :param request: data that must be passed: access token.
        :return: 400 status code if a user with such an id does not exist,
        200 and list of recommendations if everything is ok
        """
        try:
            user = get_user_from_token(request.headers['Authorization'])
        except ObjectDoesNotExist:
            return Response({'error': 'User with such an id does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        value = process_users(user.experience, user.vacancy)
        return Response({'scoring_result': value}, status=status.HTTP_200_OK)
