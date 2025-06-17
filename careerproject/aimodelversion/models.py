from django.db import models

class AIModelVersion(models.Model):
    MODEL_CHOICES = [
        ('CAREER_MATCH', 'Career Matching'),
        ('SKILL_EXTRACT', 'Skill Extraction'),
        ('PERSONALITY', 'Personality Analysis'),
    ]

    name = models.CharField(max_length=100)
    model_type = models.CharField(max_length=50, choices=MODEL_CHOICES)
    version = models.CharField(max_length=50)
    path = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    performance_metrics = models.JSONField(default=dict)
    training_data = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('name', 'version')

    def __str__(self):
        return f"{self.name} v{self.version}"

class ModelTrainingLog(models.Model):
    model_version = models.ForeignKey(AIModelVersion, on_delete=models.CASCADE)
    training_start = models.DateTimeField()
    training_end = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='RUNNING')
    metrics = models.JSONField(default=dict)
    logs = models.TextField(blank=True)

    class Meta:
        ordering = ['-training_start']

    def __str__(self):
        return f"Training {self.model_version} - {self.status}"