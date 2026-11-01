from django import forms
from .models import Plants, CareSchedule
from devices.models import ESPDevice

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plants
        fields = ['name', 'watering_interval', 'notes', 'device']

class PlantDeviceForm(forms.ModelForm):
    class Meta:
        model = Plants
        fields = ("device",)

class ControllerForm(forms.ModelForm):
    class Meta:
        model = ESPDevice
        fields = ("device_id", "name")


class PlantForControllerForm(forms.ModelForm):
    class Meta:
        model = Plants
        fields = ("name", "last_watered", "watering_interval", "notes")