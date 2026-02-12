from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

from blog.views import blog_list, post_create
from account.views import main, profile_view, home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('haberler/', include('haberler.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='account/logged_out.html'), name='logout'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='account/passwordreset.html'), name='password_reset'),
    path('accounts/password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='account/passwordresetdone.html'), name='password_reset_done'),
    path('accounts/profile/', profile_view, name='current_user_profile'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('blog_list/', blog_list, name='blog_list'),
    path('blog/', include('blog.urls')),
    path('main/', main, name='main'),
    path('', home, name='home'),
    path('new/', post_create, name='post_create'),
    path('tinymce/', include('tinymce.urls')),
    path('users/', include('account.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('__reload__/', include('django_browser_reload.urls')),
    ]
