from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

class CustomLoginView(LoginView):
    template_name = 'account/login.html'

@login_required
def profile_view(request):
    return render(request, 'account/profile.html', {'user': request.user})
