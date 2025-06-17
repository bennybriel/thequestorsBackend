from django.db import models
from django.contrib.auth import get_user_model
from careers.models import Career

User = get_user_model()

class UserProfile(models.Model):
    HOBBY_CATEGORIES = [
        ('ART', 'Arts & Creativity'),
        ('TECH', 'Technology'),
        ('OUT', 'Outdoor'),
        ('SOC', 'Social'),
        ('SPORT', 'Sports'),
        ('GAME', 'Gaming'),
        ('READ', 'Reading'),
        ('MUSIC', 'Music'),
        ('OTHER', 'Other'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    hobbies = models.TextField(blank=True)
    hobby_categories = models.JSONField(default=list)
    happy_activities = models.TextField(blank=True)
    personal_vision = models.TextField(blank=True)
    personality_type = models.CharField(max_length=10, blank=True)
    career_goals = models.TextField(blank=True)
    current_career = models.ForeignKey(
        Career,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    skills = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"