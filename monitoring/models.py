from django.db import models

class DeviceeReading(models.Model):

    device = models.ForeignKey('devices.Device', on_delete=models.CASCADE, related_name='readings')
    power = models.FloatField(help_text="القدرة اللحظية بالواط (W)")
    voltage = models.FloatField(help_text="الجهد بالفولت (V)")
    current = models.FloatField(help_text="التيار بالآمبير (A)")
    today_kwh = models.FloatField(default=0.0, help_text="الاستهلاك اليومي (kWh)")
    is_on = models.BooleanField(default=True, help_text="حالة القابس (شغال/طافي)")
    recorded_at = models.DateTimeField(auto_now_add=True, help_text="وقت القراءة")

    def __str__(self):
        return f"{self.device.name} - {self.power}W ({self.recorded_at.strftime('%Y-%m-%d %H:%M')})"

    class Alert(models.Model):
     SEVERITY_CHOICES = [
        ('critical', 'Critical'),
        ('warning', 'Warning'),
    ]

     device = models.ForeignKey('devices.Device', on_delete=models.CASCADE, related_name='alerts')
     message = models.CharField(max_length=255, help_text="Alert message")
     severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='warning')
     is_resolved = models.BooleanField(default=False, help_text="Is the issue fixed?")
     created_at = models.DateTimeField(auto_now_add=True)

     class Meta:
        ordering = ['-created_at'] 

     def __str__(self):
        return f"{self.device.name} - {self.severity}: {self.message}"