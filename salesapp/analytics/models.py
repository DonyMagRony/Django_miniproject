# analytics/models.py
from django.db import models
from userManagement.models import CustomUser


class Report(models.Model):
    REPORT_TYPES = [
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
        ('CUSTOM', 'Custom')
    ]

    report_type = models.CharField(max_length=7, choices=REPORT_TYPES)
    content = models.JSONField()
    generated_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    generated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, default='COMPLETED')

    class Meta:
        ordering = ['-generated_at']


class TradingVolumeSnapshot(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    total_volume = models.DecimalField(max_digits=15, decimal_places=2)
    average_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(fields=['timestamp', 'product']),
        ]