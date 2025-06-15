from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def main(request):
    return HttpResponse("Hello from main view!")


class CustomLoginView(LoginView):
    template_name = 'account/login.html'

@login_required
def profile_view(request):
    return render(request, 'account/profile.html', {'user': request.user})
