from django.shortcuts import render

def home_view(request):
    return render(request,'dashboard/home.html')

def alerts_view(request):
    return render(request,'dashboard/alerts.html')

from django.shortcuts import render


from django.shortcuts import render


def devices_view(request):
    # Temporary demo data; replaced later by data from the database.
    devices = [
        {'device_id': 'DW-01', 'name': 'Dishwasher', 'device_type': 'Dishwasher', 'kind': 'dishwasher',
         'location': 'Kitchen', 'rated_power': 1900, 'plug_id': '1000abcd12',
         'status': 'running', 'status_label': 'Running', 'power': 1240, 'voltage': 231, 'current': 5.4},
        {'device_id': 'FR-01', 'name': 'Refrigerator', 'device_type': 'Refrigerator', 'kind': 'fridge',
         'location': 'Kitchen', 'rated_power': 150, 'plug_id': '',
         'status': 'idle', 'status_label': 'Idle', 'power': 8, 'voltage': 230, 'current': 0.1},
        {'device_id': 'WM-01', 'name': 'Washing Machine', 'device_type': 'Washing Machine', 'kind': 'washer',
         'location': '', 'rated_power': '', 'plug_id': '',
         'status': 'offline', 'status_label': 'Offline', 'power': 0, 'voltage': 0, 'current': 0},
    ]
    return render(request, 'dashboard/devices.html', {'devices': devices})


def device_add_view(request):
    # For now we only receive the data; saving to the database comes next.
    received = request.POST if request.method == 'POST' else None
    return render(request, 'dashboard/device_add.html', {'received': received})