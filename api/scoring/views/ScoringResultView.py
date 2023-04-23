from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.scoring.utils import get_user_from_token, get_scoring_verdict


class ScoringResultView(RetrieveAPIView):
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

        return Response({'verdict': get_scoring_verdict(user.scoring_value)}, status=status.HTTP_200_OK)
