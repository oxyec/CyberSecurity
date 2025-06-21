from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, UserProfile, UserSettings

@receiver(post_save, sender=CustomUser)
def create_user_profile_and_settings(_sender, instance, created, **_kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        UserSettings.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile_and_settings(_sender, instance, **_kwargs):
    instance.profile.save()
    instance.usersettings.save()

