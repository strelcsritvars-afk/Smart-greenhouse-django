from django.urls import path
from .views import ESPDeviceListCreateView, TelemetryDataListCreateView

from dashboard.views import dashboard_data


urlpatterns = [
    path('devices/', ESPDeviceListCreateView.as_view(), name='device-list-create'),
    path('telemetry/', TelemetryDataListCreateView.as_view(), name='telemetry-list-create'),
    path('dashboard/', dashboard_data, name='dashboard'),
]