from django.db import models
from .base import TimeStampedModel

class CareerPath(TimeStampedModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    required_skills = models.JSONField(default=list)
    salary_range = models.CharField(max_length=100)
    job_outlook = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)

class ProfessionalQualification(TimeStampedModel):
    career_path = models.ForeignKey(CareerPath, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    description = models.TextField()
    exam_requirements = models.TextField()
    average_salary_boost = models.DecimalField(max_digits=5, decimal_places=2)
    marketability_boost = models.DecimalField(max_digits=5, decimal_places=2)