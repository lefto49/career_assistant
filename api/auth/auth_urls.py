from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path

from api.auth.views.ConfirmEmailView import ConfirmEmailView
from api.auth.views.GetConfirmationCodeView import GetConfirmationCodeView
from api.auth.views.GetResetLinkView import GetResetLinkView
from api.auth.views.LoginView import LoginView
from api.auth.views.PasswordResetView import PasswordResetView

urlpatterns = [
    path('get-confirmation-code/', GetConfirmationCodeView.as_view()),
    path('confirm-email/', ConfirmEmailView.as_view()),
    path('login/', LoginView.as_view()),
    path('refresh-token/', TokenRefreshView.as_view()),
    path('get-reset-link/', GetResetLinkView.as_view()),
    path('password-reset/', PasswordResetView.as_view())
]
