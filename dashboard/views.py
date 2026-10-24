from django.shortcuts import render


def devices_view(request):
    # بيانات تجريبية مؤقتة، تُستبدل لاحقاً ببيانات من قاعدة البيانات
    devices = [
        {
            'device_id': 'DW-01', 'name': 'غسالة الصحون', 'kind': 'dishwasher',
            'brand': 'Bosch', 'model_name': 'SMS25', 'rated_power': 1900,
            'status': 'running', 'status_label': 'يعمل',
            'power': 1240, 'voltage': 231, 'current': 5.4,
        },
        {
            'device_id': 'FR-01', 'name': 'الثلاجة', 'kind': 'fridge',
            'brand': 'LG', 'model_name': 'GN-B', 'rated_power': 150,
            'status': 'idle', 'status_label': 'انتظار',
            'power': 8, 'voltage': 230, 'current': 0.1,
        },
        {
            'device_id': 'WM-01', 'name': 'الغسالة', 'kind': 'washer',
            'brand': 'Samsung', 'model_name': 'WW90', 'rated_power': 2100,
            'status': 'offline', 'status_label': 'غير متصل',
            'power': 0, 'voltage': 0, 'current': 0,
        },
    ]
    return render(request, 'dashboard/devices.html', {'devices': devices})


def device_add_view(request):
    # مؤقتاً: نستقبل البيانات فقط، والحفظ في قاعدة البيانات في الخطوة التالية
    received = request.POST if request.method == 'POST' else None
    return render(request, 'dashboard/device_add.html', {'received': received})