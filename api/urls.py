from django.urls import path

from .views import CreateUserView, RetrieveUpdateUserView, LoginView, PasswordResetView, ValidateResetPasswordView

urlpatterns = [
    path('signup/', CreateUserView.as_view()),
    path('profile/', RetrieveUpdateUserView.as_view()),
    path('login/', LoginView.as_view()),
    path('password_reset/', PasswordResetView.as_view()),
    path('password_reset_confirmed/', ValidateResetPasswordView.as_view())
]
