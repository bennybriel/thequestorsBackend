from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    skills = models.JSONField(default=list, blank=True)
    is_mentor = models.BooleanField(default=False)
    mentor_expertise = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.username