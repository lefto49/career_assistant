from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import CreateUserView, RetrieveUpdateUserView, LoginView, PasswordResetView, ConfirmEmailView

urlpatterns = [
    path('signup/', CreateUserView.as_view()),
    path('confirm_email/', ConfirmEmailView.as_view()),
    path('profile/', RetrieveUpdateUserView.as_view()),
    path('login/', LoginView.as_view()),
    path('refresh_token/', TokenRefreshView.as_view()),
    path('password_reset/', PasswordResetView.as_view())
]
