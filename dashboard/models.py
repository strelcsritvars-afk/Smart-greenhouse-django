import uuid
from django.db import models
from django.conf import settings

from devices.models import ESPDevice

class Plants(models.Model):
    """
    A plant model that represents a plant in the system.
    """

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Links models together, creating a one-to-many relationship (one user can have many plants)
        on_delete=models.CASCADE,
        related_name='plants',
    )
    name = models.CharField(
        max_length=50,
        help_text="Plant species",
        default="New Plant"
    )

    last_watered = models.DateTimeField(
        null = True,
        blank = True,
        help_text="Time when plant was last watered",
    )

    watering_interval = models.IntegerField(
        help_text="Number of days between watering",
    )

    notes = models.TextField(
        null = True,
        blank = True,
        help_text="Additional notes about the plant",
    )

    device = models.ForeignKey(
        ESPDevice,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="plants",
        help_text="Which device is plant connected to"
    )

    def __str__(self): #Returns human readable string
        return f"{self.name}"

CARE_TASK_CHOICES = [
    ("water", "Watering"),
    ("fertilize", "Fertilizing"),
    ("prune", "Pruning"),
]

class CareSchedule(models.Model):
    plant = models.ForeignKey(
        Plants,
        on_delete=models.CASCADE,
        related_name="care_schedules",
        help_text="Which plant this care schedule belongs to"
    )

    task = models.CharField(
        max_length=20,
        choices=CARE_TASK_CHOICES,
        help_text="What type of care")

    interval_days = models.IntegerField(
        help_text="Number of days between care"
    )

    due_date = models.DateField(
        help_text="Next due date for care")

class CareLog(models.Model):
    plant = models.ForeignKey(
        Plants,
        on_delete=models.CASCADE,
        related_name="care_logs",
        help_text="Which plant this care log belongs to"
    )

    task = models.CharField(
        max_length=20,
        choices=CARE_TASK_CHOICES,
        help_text="What type of care was performed"
    )

    done_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when care was performed"
    )

    notes = models.TextField(
        null=True,
        blank = True,
        help_text="Additional notes about the care performed"
    )