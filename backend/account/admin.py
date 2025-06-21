from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import UserProfile, UserSettings, UserActivity

CustomUser = get_user_model()

# CustomUser unregister işlemi
try:
    admin.site.unregister(CustomUser)
except admin.sites.NotRegistered:
    pass

# UserSettings unregister işlemi
try:
    admin.site.unregister(UserSettings)
except admin.sites.NotRegistered:
    pass

# UserActivity unregister işlemi
try:
    admin.site.unregister(UserActivity)
except admin.sites.NotRegistered:
    pass


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'username', 'email', 'full_name', 'student_id',
        'github_link', 'is_staff', 'is_active', 'date_joined'
    )
    list_filter = ('is_active', 'is_staff', 'date_joined', 'last_login')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('student_id', 'github_handle'),
            'classes': ('wide',)
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('student_id', 'github_handle'),
            'classes': ('wide',)
        }),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name',
                     'student_id', 'github_handle')
    ordering = ('username',)
    readonly_fields = ('date_joined', 'last_login')

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or "-"

    full_name.short_description = "Full Name"

    def github_link(self, obj):
        if obj.github_handle:
            return format_html(
                '<a href="https://github.com/{}" target="_blank">{}</a>',
                obj.github_handle, obj.github_handle
            )
        return "-"

    github_link.short_description = "GitHub Profile"


##@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'website_link', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'location', 'website', 'bio')
    list_filter = ('created_at', 'updated_at', 'location')
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ['user']

    def website_link(self, obj):
        if obj.website:
            return format_html('<a href="{}" target="_blank">{}</a>', obj.website, obj.website)
        return "-"

    website_link.short_description = "Website"


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'receive_newsletter', 'dark_mode')  # modified_at kaldırıldı
    list_filter = ('receive_newsletter', 'dark_mode')           # modified_at kaldırıldı
    search_fields = ('user__username', 'user__email')
    autocomplete_fields = ['user']
    list_per_page = 25


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_login', 'last_activity', 'is_active_now')
    list_filter = ('last_activity', 'last_login')
    search_fields = ('user__username', 'user__email')
    ordering = ('-last_activity',)
    readonly_fields = ('last_login', 'last_activity')
    autocomplete_fields = ['user']

    def is_active_now(self, obj):
        if obj.last_activity:
            time_diff = timezone.now() - obj.last_activity
            if time_diff.total_seconds() < 300:  # 5 dakika
                return format_html('<span style="color: green;">●</span> Online')
        return format_html('<span style="color: red;">●</span> Offline')

    is_active_now.short_description = "Status"


admin.site.site_header = "User Management System"
admin.site.site_title = "User Management Admin Portal"
admin.site.index_title = "Welcome to User Management Portal"
admin.site.enable_nav_sidebar = False  # Sidebar'ı kapattık
admin.site.site_url = None  # Site ana sayfası linki kapatıldı
