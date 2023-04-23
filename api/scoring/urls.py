from django.urls import path
from api.scoring.views.ScoringResultView import ScoringResultView
from api.scoring.views.SetScoringView import SetScoringView

urlpatterns = [
    path('result/', ScoringResultView.as_view()),
    path('set/', SetScoringView.as_view())
]
