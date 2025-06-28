from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .base import TimeStampedModel
from django.conf import settings

class UserProfile(TimeStampedModel):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hobbies = models.JSONField(default=list, blank=True)
    passions = models.JSONField(default=list, blank=True)
    skills = models.JSONField(default=list, blank=True)
    vision = models.TextField(blank=True)
    dream = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()