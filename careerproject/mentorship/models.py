from django.db import models
from django.contrib.auth import get_user_model
from careers.models import Career

User = get_user_model()

class MentorshipConnection(models.Model):
    PENDING = 'PENDING'
    ACTIVE = 'ACTIVE'
    COMPLETED = 'COMPLETED'
    DECLINED = 'DECLINED'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACTIVE, 'Active'),
        (COMPLETED, 'Completed'),
        (DECLINED, 'Declined'),
    ]

    mentor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='mentor_connections'
    )
    mentee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='mentee_connections'
    )
    career = models.ForeignKey(
        Career,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    goals = models.TextField(blank=True)

    class Meta:
        unique_together = ('mentor', 'mentee', 'career')

    def __str__(self):
        return f"{self.mentor} -> {self.mentee} ({self.status})"

class MentorshipMessage(models.Model):
    connection = models.ForeignKey(
        MentorshipConnection,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message from {self.sender} at {self.timestamp}"