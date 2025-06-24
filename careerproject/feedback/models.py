from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Feedback(models.Model):
    RATING_CHOICES = [
        (1, 'Very Poor'),
        (2, 'Poor'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Excellent'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Feedback'

    def __str__(self):
        return f"Feedback #{self.id} by {self.user.username}"

    @property
    def rating_display(self):
        return dict(self.RATING_CHOICES).get(self.rating, '')