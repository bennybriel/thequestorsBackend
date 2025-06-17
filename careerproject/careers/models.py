from django.db import models

class Career(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    required_skills = models.JSONField(default=list)
    recommended_skills = models.JSONField(default=list)
    salary_range_min = models.IntegerField()
    salary_range_max = models.IntegerField()
    growth_outlook = models.FloatField()
    demand_level = models.CharField(max_length=20, choices=[
        ('HIGH', 'High Demand'),
        ('MEDIUM', 'Medium Demand'),
        ('LOW', 'Low Demand'),
    ])
    education_requirements = models.TextField()
    typical_pathway = models.JSONField(default=list)
    related_hobbies = models.JSONField(default=list)

    def __str__(self):
        return self.title

class LearningResource(models.Model):
    RESOURCE_TYPES = [
        ('COURSE', 'Online Course'),
        ('BOOK', 'Book'),
        ('BOOT', 'Bootcamp'),
        ('DEG', 'Degree Program'),
        ('TUT', 'Tutorial'),
    ]

    career = models.ForeignKey(Career, related_name='resources', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    url = models.URLField()
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES)
    provider = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    duration = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.title} for {self.career.title}"