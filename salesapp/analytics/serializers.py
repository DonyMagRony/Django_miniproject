# analytics/serializers.py
from rest_framework import serializers
from .models import Report, TradingVolumeSnapshot

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'report_type', 'start_date', 'end_date', 'status', 'generated_at']
        read_only_fields = ['status', 'generated_at']

class TradingVolumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradingVolumeSnapshot
        fields = ['timestamp', 'product', 'total_volume', 'average_price']