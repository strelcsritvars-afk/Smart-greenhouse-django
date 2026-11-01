from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator
from datetime import timedelta
from django.utils import timezone
from django.db.models import Prefetch

from devices.models import ESPDevice, TelemetryData
import devices.models as models

from .models import *
from .forms import *

# Dashboard view

def dashboard_data(request):

    if not request.user.is_authenticated:
        return redirect('login')

    period = request.GET.get("period", "week")
    today = timezone.localdate()

    if period == "day":
        start_date = today
    elif period == "week":
        start_date = today - timedelta(days=today.weekday())
    elif period == "month":
        period = "month"
        start_date = today.replace(day=1)
    else:
        period = "all"
        start_date = timezone.datetime.min.date()


    #List for humidity readings from the database
    readings = list(
        TelemetryData.objects
        .filter(timestamp__date__gte=start_date)
        .order_by("timestamp")[:100]
        .values("timestamp", 
        "air_humidity",
        "soil_humidity",
        "air_temperature"))

# Pages
    paginator = Paginator(readings, 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    page_readings = list(page_obj.object_list)

    latest = page_readings[-1] if page_readings else None

    context = {
        "readings": readings,
        "page_readings" : page_readings,
        "page_obj" : page_obj,
        "selected_period" : period,
        "air_humidity": (readings[-1]["air_humidity"] if readings else None),
        "soil_humidity": (readings[-1]["soil_humidity"] if readings else None),
        "air_temperature": (readings[-1]["air_temperature"] if readings else None),
    }

    return render(request, "dashboard_main.html", context)

# Plants view
def plants_main(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, "plants_main.html", {"plants": Plants.objects.select_related("device").all(), 
                                                "edit_mode": request.GET.get("edit") == "1",})

# Create a new plant

def plant_add(request):
    form = PlantForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        plant = form.save(commit=False)
        plant.owner = request.user
        plant.save()
        return redirect("plants")

    return render(request, "plants_form.html", {
        "form": form,
        "title": "Add plant",
        "cancel_url": "plants",
    })

# Edit an existing plant
@login_required
def plant_edit(request, pk):
    plant = get_object_or_404(Plants, pk=pk)
    form = PlantForm(request.POST or None, instance=plant)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("plants")

    return render(request, "plants_form.html", {
        "form" : form,
        "title" : "Edit plant",
        "cancel_url" : "plants",
    })

# Delete a plant
@login_required
@require_POST
def plant_delete(request, pk):
    plant = get_object_or_404(Plants, pk=pk)
    plant.delete()
    return redirect("plants")

# Assign a device to a plant

@login_required
@require_POST
def plant_assign_device(request, pk):
    plant = get_object_or_404(Plants, pk=pk)
    device_id = request.POST.get("device_id")
    device = get_object_or_404(ESPDevice, device_id=device_id)
    plant.device = device
    plant.save()
    return redirect("plants?edit=1")

#Controller view
@login_required
def controllers_main(request):
    latest_reading = TelemetryData.objects.order_by("-timestamp")[:1]

    controllers = ESPDevice.objects.prefetch_related(
        "plants",
        Prefetch(
            "telemetry",
            queryset=latest_reading,
            to_attr="latest_readings",
        ),
    )

    return render(request, "controllers_main.html", {
        "controllers": controllers,
        "edit_mode": request.GET.get("edit") == "1",
    })


# Add a controller
@login_required
def controller_add(request):
    form = ControllerForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("controllers")

    return render(request, "plants_form.html", {
        "form": form,
        "title": "Add controller",
        "cancel_url": "controllers",
    })


# Edit a controller
@login_required
def controller_edit(request, pk):
    controller = get_object_or_404(ESPDevice, pk=pk)
    form = ControllerForm(request.POST or None, instance=controller)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("controllers")

    return render(request, "plants_form.html", {
        "form": form,
        "title": "Edit controller",
        "cancel_url": "controllers",
    })


# Delete a controller 
@login_required
@require_POST
def controller_delete(request, pk):
    controller = get_object_or_404(ESPDevice, pk=pk)
    controller.delete()
    return redirect("controllers")


# Add a plant and link it to this controller
@login_required
def controller_add_plant(request, pk):
    controller = get_object_or_404(ESPDevice, pk=pk)
    form = PlantForControllerForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        plant = form.save(commit=False)
        plant.owner = request.user
        plant.device = controller
        plant.save()
        return redirect("controllers")

    return render(request, "plants_form.html", {
        "form": form,
        "title": f"Add plant to {controller.name}",
        "cancel_url": "controllers",
    })
