from django.db import models
from users.models import CustomUser
from careers.models import Career

class CareerMatch(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    career = models.ForeignKey(Career, on_delete=models.CASCADE)
    match_score = models.FloatField()
    skill_match = models.JSONField(default=list)
    skill_gaps = models.JSONField(default=list)
    explanation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user_feedback = models.IntegerField(null=True, blank=True)
    feedback_notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('user', 'career')

    def __str__(self):
        return f"{self.user} - {self.career} ({self.match_score}%)"

class PredictionSession(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    input_data = models.JSONField()
    results = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Session {self.id} for {self.user}"