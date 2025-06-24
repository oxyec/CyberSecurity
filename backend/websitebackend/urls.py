"""
URL configuration for websitebackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.http import HttpResponse

from blog.views import blog_list, post_create
from account.views import main

from django.urls import path
#from .views import clear_cache


def home_view(_):
    return HttpResponse("Ana sayfaya hoşgeldiniz!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('haberler/', include('haberler.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/passwordreset.html'), name='password_reset'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='account/passwordreset.html'), name='password_reset'),
    path('accounts/password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='account/passwordresetdone.html'), name='password_reset_done'),
    #path("accounts/", include("django.contrib.auth.urls")),
    path('blog_list/', blog_list , name='logout'),
    path('main/', main , name='logout'),
    path('', home_view, name='home'),
    path('new/', post_create, name='post_create'),
    path("__reload__/", include("django_browser_reload.urls")),
    #path('account/', include('account.urls')),
    path('blog/', include('blog.urls')),
]


#urlpatterns += [
    #path('clear-cache/', clear_cache, name='clear_cache'),
#]
