from django.urls import path

from api.auth.views.CreateUserView import CreateUserView
from api.auth.views.RetrieveUpdateUserView import RetrieveUpdateUserView

urlpatterns = [
    path('create/', CreateUserView.as_view()),
    path('info/', RetrieveUpdateUserView.as_view())
]
