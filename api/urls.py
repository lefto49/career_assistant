from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import CreateUserView, RetrieveUpdateUserView, LoginView, PasswordResetView, ValidateResetPasswordView

urlpatterns = [
    path('signup/', CreateUserView.as_view()),
    path('profile/', RetrieveUpdateUserView.as_view()),
    path('login/', LoginView.as_view()),
    path('refresh_token/', TokenRefreshView.as_view()),
    path('password_reset/', PasswordResetView.as_view()),
    path('password_reset_confirmed/', ValidateResetPasswordView.as_view())
]
