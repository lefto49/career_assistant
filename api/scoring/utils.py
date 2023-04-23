from jwt import decode

from django.core.exceptions import ObjectDoesNotExist

import career_assistant.settings
from api.models import User


def get_user_from_token(token):
    token = token[7:]
    uid = decode(token, career_assistant.settings.SECRET_KEY, algorithms=['HS256'])['user_id']

    if not User.objects.filter(id=uid).exists():
        raise ObjectDoesNotExist

    return User.objects.get(id=uid)


def get_scoring_verdict(scoring_value):
    if scoring_value <= 0.02:
        verdict = 'Unfortunately, right now you are not ready to apply for a desired vacancy.' \
                  '\nBut do not get sad: we already have recommendations that can help boost your skills! ' \
                  '\nClick on Recommendations for more details.'
    elif scoring_value <= 0.09:
        verdict = 'You already have some skills that make you suitable for junior positions!' \
                  '\nHowever, we suggest you develop them even further by doing various activities.' \
                  '\nClick on Recommendations for more details.'
    elif scoring_value <= 0.2:
        verdict = 'Wow, you are quite a good specialist in your field! \nDo not stop on what you have already achieved' \
                  'and continue improving your skills even further by participating in the recommended activities. ' \
                  '\nClick on Recommendations for more details.'
    else:
        verdict = 'You could be called an expert in your field! \nIt is amazing that you strive for improving your skill' \
                  ' even further. Luckily, we have alredy prepared some vacancies, courses and cup specially for you!' \
                  'and continue improving your skills even further by participating in the recommended activities. ' \
                  '\nClick on Recommendations for more details.'

    return verdict
