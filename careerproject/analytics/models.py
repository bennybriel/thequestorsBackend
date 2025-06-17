from django.db import models
from django.contrib.auth import get_user_model
from careers.models import Career

User = get_user_model()

class UserBehavior(models.Model):
    ACTION_CHOICES = [
        ('VIEW_CAREER', 'Viewed Career'),
        ('CLICK_RESOURCE', 'Clicked Resource'),
        ('SAVE_CAREER', 'Saved Career'),
        ('SHARE_CAREER', 'Shared Career'),
        ('LOGIN', 'Logged In'),
        ('SEARCH', 'Performed Search'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    target_id = models.IntegerField(null=True, blank=True)  # Career ID, Resource ID, etc.
    target_type = models.CharField(max_length=50, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict)  # Additional context (e.g., search query)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['action', 'timestamp']),
        ]
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user} - {self.action} at {self.timestamp}"

class CareerTrend(models.Model):
    career = models.ForeignKey(Career, on_delete=models.CASCADE)
    date = models.DateField()
    demand_score = models.FloatField()  # 0-100 scale
    salary_trend = models.FloatField()  # % change
    popularity = models.FloatField()  # 0-100 scale (based on user interactions)
    search_volume = models.IntegerField(default=0)

    class Meta:
        unique_together = ('career', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.career.title} Trend ({self.date})"