<<<<<<< Updated upstream
from django.contrib.auth.views import LoginView, PasswordResetView
from django.shortcuts import render


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/passwordreset.html'
=======
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
>>>>>>> Stashed changes
