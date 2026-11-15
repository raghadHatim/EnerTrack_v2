from .ewelink.client import Client
from devices.models import Device
from .models import DeviceeReading 
import asyncio
from django.conf import settings

# Connecting to eWeLink servers and fetching data
async def fetch_all_plugs_data():
    client=None
    try:
        client = Client(email=settings.EWELINK_EMAIL, password=settings.EWELINK_PASSWORD, region=settings.EWELINK_REGION)
        await client.login()

        plugs_map = {}
        for plug in client.devices:
             plugs_map[plug.id] = {
                    "online": plug.online,
                    "params": plug.params
                }
        return plugs_map 

    except Exception as e:
        print(f"Error connecting to eWeLink: {e}")
        return {}

    finally:
        current_task = asyncio.current_task()
        bg_tasks = [task for task in asyncio.all_tasks() if task is not current_task]
        for task in bg_tasks:
            task.cancel()
        if bg_tasks:
            await asyncio.gather(*bg_tasks, return_exceptions=True)
        if client:
            if client.ws and not client.ws.closed:
                await client.ws.close()
            if getattr(client.http, "session", None) and not client.http.session.closed:
                await client.http.session.close()

# Checking data quality, transforming it, and saving it to the database
def save_device_reading(device_obj, plug_data):
    # To avoid recording false zero readings in the event of a power or internet outage at the plug
    if not plug_data or not plug_data.get("online"):
     return None
    
    params = plug_data.get("params", {})
    power = float(params.get("power") or 0.0)
    voltage = float(params.get("voltage") or 0.0)
    current = float(params.get("current") or 0.0)
    today_kwh = float(params.get("dayKwh") or 0.0)
    is_on = (params.get("switch") == "on")

    return DeviceeReading.objects.create(
        device=device_obj,
        power=power,
        voltage=voltage,
        current=current,
        today_kwh=today_kwh,
        is_on=is_on
    )

# Fetch and save the latest smart plug reading for a single device (ex: manual refresh)
def sync_device_reading(device_obj):
    if not device_obj.smart_plug_id:
        return None
    plugs_map = asyncio.run(fetch_all_plugs_data())
    plug_data = plugs_map.get(device_obj.smart_plug_id)
    return save_device_reading(device_obj, plug_data)

# Sync the latest energy readings from eWeLink cloud for all configured devices in a single request
def sync_all_devices():
    devices = Device.objects.exclude(smart_plug_id__isnull=True).exclude(smart_plug_id="")
    if not devices.exists():
        return []

    plugs_map = asyncio.run(fetch_all_plugs_data())
    saved_readings = []
    for device_obj in devices:
        plug_data = plugs_map.get(device_obj.smart_plug_id)
        reading = save_device_reading(device_obj, plug_data)
        if reading:
            saved_readings.append(reading)
    return saved_readings
