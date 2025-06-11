from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin

# ------------------------------
# MODELLER
# ------------------------------

class CustomUser(AbstractUser):
    student_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    github_handle = models.CharField(max_length=39, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserSettings(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    receive_newsletter = models.BooleanField(default=False)
    dark_mode = models.BooleanField(default=False)

class UserActivity(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    last_login = models.DateTimeField(null=True, blank=True)
    last_activity = models.DateTimeField(null=True, blank=True)

# ------------------------------
# ADMİN KAYITLARI
# ------------------------------

@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    readonly_fields = ()
    list_display = ('user', 'receive_newsletter', 'dark_mode')
    list_filter = ('receive_newsletter', 'dark_mode')

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'student_id', 'github_handle', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_login', 'last_activity')
    readonly_fields = ('last_login', 'last_activity')
    list_filter = ('last_login', 'last_activity')
    search_fields = ('user__username', 'user__email')
