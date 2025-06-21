from django.db import models
from django.utils import timezone
from .constants.status import Status
from django.core.exceptions import ValidationError

class School(models.Model):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    ]

    name = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    guid = models.CharField(max_length=255, unique=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=ACTIVE,
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='unique_school_name',
                condition=models.Q(status='active'),
                violation_error_message="School with this name already exists"
            ),
            models.UniqueConstraint(
                fields=['website'],
                name='unique_school_website',
                condition=models.Q(status='active'),
                violation_error_message="School with this website already exists"
            )
        ]


class Course(models.Model):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    ]

    name = models.CharField(max_length=255)
    guid = models.CharField(max_length=255, unique=True)
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=ACTIVE,
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} ({self.school.name})"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'school'],
                name='unique_course_per_school',
                condition=models.Q(status='active'),
                violation_error_message="This course already exists in the specified school"
            )
        ]

class Subject(models.Model):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    ]

    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=ACTIVE,
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Subjects"


class UTMERequirement(models.Model):
    REQUIRED = 'required'
    NOT_REQUIRED = 'not_required'
    RECOMMENDED = 'recommended'
    REQUIRED_STATUS_CHOICES = [
        (REQUIRED, 'Required'),
        (NOT_REQUIRED, 'Not Required'),
        (RECOMMENDED, 'Recommended'),
    ]

    ACTIVE = 'active'
    INACTIVE = 'inactive'
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    ]

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='utme_requirements'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='utme_requirements'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='utme_requirements'
    )
    required_status = models.CharField(
    max_length=20,
    choices=REQUIRED_STATUS_CHOICES,
    # Remove the default to make it required
    blank=False,  # Explicitly make it non-blank
    null=False,   # Explicitly make it non-null
   )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=ACTIVE,
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "UTME Requirements"
        unique_together = ('school', 'course', 'subject')

class OLevelRequirement(models.Model):
    REQUIRED = 'required'
    NOT_REQUIRED = 'not_required'
    RECOMMENDED = 'recommended'
    REQUIRED_STATUS_CHOICES = [
        (REQUIRED, 'Required'),
        (NOT_REQUIRED, 'Not Required'),
        (RECOMMENDED, 'Recommended'),
    ]

    ACTIVE = 'active'
    INACTIVE = 'inactive'
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    ]

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='olevel_requirements'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='olevel_requirements'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='olevel_requirements'
    )
    required_status = models.CharField(
        max_length=20,
        choices=REQUIRED_STATUS_CHOICES,
        default=REQUIRED,
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=ACTIVE,
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "O'Level Requirements"
        unique_together = ('school', 'course', 'subject')