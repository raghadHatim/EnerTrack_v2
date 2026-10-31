from django.db import models
from django.contrib.auth.models import User

class Device(models.Model):
    DEVICE_TYPES = [
        ('dishwasher', 'Dishwasher'),
        ('refrigerator', 'Refrigerator'),
        ('washing_machine', 'Washing Machine'),
        ('air_conditioner', 'Air Conditioner'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    name = models.CharField(max_length=60, help_text="Device name")
    kind = models.CharField(max_length=20, choices=DEVICE_TYPES, help_text="Device type")
    model_name = models.CharField(max_length=40, blank=True, null=True, help_text="Model")
    rated_power = models.PositiveIntegerField(help_text="Rated power (W)")
    device_id = models.CharField(max_length=50, unique=True, help_text="Unique device ID")
    created_at = models.DateTimeField(auto_now_add=True)
    custom_type = models.CharField(max_length=100, blank=True, null=True, help_text="Custom device type if 'Other' is selected")
    smart_plug_id = models.CharField(max_length=100, blank=True, null=True, help_text="Smart plug ID for eWeLink API connection")
    location = models.CharField(max_length=100, blank=True, null=True, help_text="Device location")

    def __str__(self):
        return f"{self.name} ({self.delete})"

