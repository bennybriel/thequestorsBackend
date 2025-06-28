from django.db import models
from .base import TimeStampedModel
from .career import CareerPath

class University(TimeStampedModel):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    global_ranking = models.IntegerField()
    program_strengths = models.JSONField(default=list)
    industry_connections = models.JSONField(default=list)
    notable_alumni = models.JSONField(default=list)
    internship_opportunities = models.BooleanField()
    average_graduate_salary = models.DecimalField(max_digits=10, decimal_places=2)

class EducationPath(TimeStampedModel):
    career_path = models.ForeignKey(CareerPath, on_delete=models.CASCADE)
    degree_name = models.CharField(max_length=200)
    recommended_majors = models.JSONField(default=list)
    typical_duration = models.CharField(max_length=50)
    top_universities = models.JSONField(default=list)

class UniversityCareerPath(TimeStampedModel):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    career_path = models.ForeignKey(CareerPath, on_delete=models.CASCADE)
    strength_rating = models.DecimalField(max_digits=3, decimal_places=1)

    class Meta:
        unique_together = ('university', 'career_path')