from django.urls import path
from .views import (
    RegisterView,
    ProfileView,
    AbaListView,
    SubmitRespostasView,
    login_or_register
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('abas/', AbaListView.as_view()),
    path('submit-respostas/', SubmitRespostasView.as_view()),
    path('login-or-register/', login_or_register),
]