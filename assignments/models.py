from django.db import models
from django.utils import timezone


class Assignment(models.Model):
    class Status(models.TextChoices):
        PENDING = "Pending", "Pending"
        IN_PROGRESS = "In Progress", "In Progress"
        COMPLETED = "Completed", "Completed"


    title = models.CharField(max_length=200)
    course = models.CharField(max_length=100, blank=True)
    subject_teacher = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "assignments"


    def __str__(self):
        return self.title


    @property
    def is_overdue(self):
        """True when the due date passed and the work is not finished."""
        return (
            self.due_date < timezone.localdate()
            and self.status != self.Status.COMPLETED
        )