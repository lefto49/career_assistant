from django.urls import path

from api.recommendations.views.SetRecommendationsView import SetRecommendationsView
from api.recommendations.views.GetRecommendationsView import GetRecommendationsView

urlpatterns = [
    path('show/', GetRecommendationsView.as_view()),
    path('set/', SetRecommendationsView.as_view())
]
