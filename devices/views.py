from rest_framework import generics
from .models import ESPDevice, TelemetryData
from .serializers import ESPDeviceSerializer, TelemetryDataSerializer

# GET all devices or POST a new divce
class ESPDeviceListCreateView(generics.ListCreateAPIView):
    queryset = ESPDevice.objects.all()
    serializer_class = ESPDeviceSerializer

#Get all telemetry or POST new sensor logs from ESP32
class TelemetryDataListCreateView(generics.ListCreateAPIView):
    queryset = TelemetryData.objects.all()
    serializer_class = TelemetryDataSerializer
