from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin

# ------------------------------
# MODELS
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

    def __str__(self):
        return f"Settings for {self.user.username}"

class UserActivity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    last_login = models.DateTimeField(null=True, blank=True)
    last_activity = models.DateTimeField(null=True, blank=True)

# Yeni model: Şüpheli login girişlerini izlemek için
class LoginAttempt(models.Model):
    ip_address = models.GenericIPAddressField()
    username = models.CharField(max_length=150, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField(default=False)

    def __str__(self):
        status = "Başarılı" if self.successful else "Başarısız"
        return f"{self.timestamp} - {self.username or 'Bilinmeyen'} ({self.ip_address}) → {status}"

# ------------------------------
# ADMIN RECORDS
# ------------------------------
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'student_id', 'github_handle', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('username', 'email', 'student_id', 'github_handle')

@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    readonly_fields = ()
    list_display = ('user', 'receive_newsletter', 'dark_mode')
    list_filter = ('receive_newsletter', 'dark_mode')

def __str__(self):
    return f"Profile of {self.user.username}"

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_login', 'last_activity')
    readonly_fields = ('last_login', 'last_activity')
    list_filter = ('last_login', 'last_activity')
    search_fields = ('user__username', 'user__email')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'website', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

# LoginAttempt modeli admin paneline de ekleyelim:
@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'username', 'timestamp', 'successful')
    list_filter = ('successful', 'timestamp')
    search_fields = ('username', 'ip_address')
