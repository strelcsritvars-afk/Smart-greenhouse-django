from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator
from datetime import timedelta
from django.utils import timezone

from devices.models import TelemetryData
import devices.models as models

# Create your views here.

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

