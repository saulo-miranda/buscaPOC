from django.urls import path
from .views import SignupPageView, sign_up

urlpatterns = [
    path("signup/", sign_up(), name="signup")
]