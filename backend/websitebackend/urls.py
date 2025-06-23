from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.http import HttpResponse

from blog.views import blog_list
from account.views import main

def home_view(_):
    return HttpResponse("Ana sayfaya hoşgeldiniz!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/passwordreset.html'), name='password_reset'),
    #path("accounts/", include("django.contrib.auth.urls")),
    path('blog_list/', blog_list , name='logout'),
    path('main/', main , name='logout'),
    path('', home_view, name='home'),
    path("__reload__/", include("django_browser_reload.urls")),

  
    path('account/', include('account.urls')),
]
