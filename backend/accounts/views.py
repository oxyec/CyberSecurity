from django.contrib.auth.views import LoginView, PasswordResetView
from django.shortcuts import render


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/passwordreset.html'

def main(request):
    return render(request, 'main/navbar.html', {})