from rest_framework import serializers
from .models import ESPDevice, TelemetryData


class ESPDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ESPDevice
        fields = ['device_id', 'name', 'solenoid_open', 'last_seen']

class TelemetryDataSerializer(serializers.ModelSerializer):
    device = serializers.SlugRelatedField(
        slug_field='device_id',
        queryset=ESPDevice.objects.all()
    )

    class Meta:
        model = TelemetryData
        fields = ['id', 'device', 'soil_humidity', 'air_humidity', 'air_temperature', 'timestamp']