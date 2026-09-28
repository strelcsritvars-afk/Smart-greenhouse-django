from django.contrib import admin
from .models import ESPDevice, TelemetryData

@admin.register(ESPDevice)
class ESPDeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'device_id', 'solenoid_open', 'last_seen')
    list_editable = ('solenoid_open',)  # Allows toggling valves

@admin.register(TelemetryData)
class TelemetryDataAdmin(admin.ModelAdmin):
    list_display = ('device', 'soil_humidity', 'air_temperature', 'air_humidity', 'timestamp')
    list_filter = ('device', 'timestamp')

