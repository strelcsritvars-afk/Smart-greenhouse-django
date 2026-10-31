from django.contrib import admin
from .models import CareLog, CareSchedule, Plants


@admin.register(Plants)
class PlantsAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "device", "last_watered", "watering_interval")
    list_filter = ("owner",)
    search_fields = ("name",)


@admin.register(CareSchedule)
class CareScheduleAdmin(admin.ModelAdmin):
    list_display = ("plant", "task", "interval_days", "due_date")
    list_filter = ("task",)


@admin.register(CareLog)
class CareLogAdmin(admin.ModelAdmin):
    list_display = ("plant", "task", "done_at")
    list_filter = ("task", "done_at")
