import uuid
from django.db import models

class ESPDevice(models.Model):
    """
    Represents a physical ESP32 board in your home setup.
    Each physical board will have one row in database table.
    """
    device_id = models.CharField(
        max_length=50, 
        unique=True, 
        help_text="Unique identifier, e.g., MAC address or custom string like esp32_garden"
    )

    name = models.CharField(max_length=50, default="New ESP32 Node")

    solenoid_open = models.BooleanField(
        default=False, 
        help_text="Current state of solenoid valve"
    )
    last_seen = models.DateTimeField(auto_now=True, help_text="Automatically updates timestamp on save")

    def __str__(self): #Returns human readable string
        return f"{self.name} ({self.device_id})"


class TelemetryData(models.Model):
    """
    Stores historical sensor readings over time.
    Every single ping from an ESP32 creates a new row here.
    """
    device = models.ForeignKey(
        ESPDevice, # Links models together, creating a one-to-many relationship (one device can have many telemetry readings)
        on_delete=models.CASCADE,
        related_name='telemetry',
        help_text="Links reading directly to specific ESPDevice"
    )
    soil_humidity = models.IntegerField(help_text="Soil moisture")
    air_humidity = models.IntegerField(help_text="Air humidity")
    air_temperature = models.IntegerField(help_text="Temperature")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Automatically set")

    class Meta:
        ordering = ['-timestamp']  #Sort newest entries first by default

    def __str__(self): #Returns human readable string
        return f"{self.device.device_id} @ {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
