from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import CreateUserView, RetrieveUpdateUserView, LoginView, PasswordResetView, ConfirmEmailView, \
    GetResetLinkView, GetConfirmationCodeView, GetRecommendationsView

urlpatterns = [
    path('signup/', CreateUserView.as_view()),
    path('get-confirmation-code/', GetConfirmationCodeView.as_view()),
    path('confirm-email/', ConfirmEmailView.as_view()),
    path('profile/', RetrieveUpdateUserView.as_view()),
    path('login/', LoginView.as_view()),
    path('refresh-token/', TokenRefreshView.as_view()),
    path('get-reset-link/', GetResetLinkView.as_view()),
    path('password-reset/', PasswordResetView.as_view()),
    path('get-recommendations/', GetRecommendationsView.as_view())
]
