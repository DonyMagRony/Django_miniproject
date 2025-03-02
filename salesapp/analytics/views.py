# analytics/views.py
from django.utils import timezone
from django.db.models import Sum, Count, F, ExpressionWrapper, DecimalField
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Report
from .serializers import ReportSerializer
from sales.models import SalesOrder
from trade.models import Transaction
from datetime import timedelta
from django.core.cache import cache


class AnalyticsDashboard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Simple dashboard with basic metrics
        data = {
            'total_sales': self.get_total_sales(),
            'total_trades': self.get_total_trades(),
            'top_products': self.get_top_products(),
        }
        return Response(data)

    def get_total_sales(self):
        return SalesOrder.objects.aggregate(
            total_sales=Sum('total')
        )['total_sales'] or 0

    def get_total_trades(self):
        return Transaction.objects.count()

    def get_top_products(self):
        return SalesOrder.objects.values(
            'items__product__name'
        ).annotate(
            total_sold=Sum('items__quantity')
        ).order_by('-total_sold')[:5]


class BasicSalesReport(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Simple sales report with date filtering
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        sales = SalesOrder.objects.all()

        if start_date:
            sales = sales.filter(created_at__gte=start_date)
        if end_date:
            sales = sales.filter(created_at__lte=end_date)

        report_data = {
            'total_sales': sales.aggregate(total=Sum('total'))['total'] or 0,
            'total_orders': sales.count(),
            'average_order': sales.aggregate(
                avg=ExpressionWrapper(
                    Sum('total') / Count('id'),
                    output_field=DecimalField()
                )
            )['avg'] or 0
        }

        return Response(report_data)


class TradingVolumeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Simple volume view with basic time filtering
        days = int(request.query_params.get('days', 7))

        volume = Transaction.objects.filter(
            timestamp__gte=timezone.now() - timedelta(days=days)
        ).aggregate(
            total_volume=Sum('quantity'),
            total_value=Sum(F('quantity') * F('price'))
        )

        return Response({
            'total_volume': volume['total_volume'] or 0,
            'total_value': volume['total_value'] or 0
        })


class SimpleProfitLossView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # Basic profit/loss calculation
        revenue = SalesOrder.objects.aggregate(total=Sum('total'))['total'] or 0
        costs = Transaction.objects.aggregate(
            total=Sum(F('quantity') * F('price'))
        )['total'] or 0

        return Response({
            'revenue': revenue,
            'costs': costs,
            'profit': revenue - costs
        })


class ReportGenerationView(generics.CreateAPIView):
    serializer_class = ReportSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        # Simple synchronous report generation
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        report_type = serializer.validated_data['report_type']
        time_range = self.get_time_range(report_type)

        # Generate report immediately
        report_data = self.generate_report(time_range)

        report = Report.objects.create(
            report_type=report_type,
            content=report_data,
            start_date=time_range['start'],
            end_date=time_range['end'],
            generated_by=request.user,
            status='COMPLETED'
        )

        return Response(
            ReportSerializer(report).data,
            status=status.HTTP_201_CREATED
        )

    def get_time_range(self, report_type):
        now = timezone.now()
        return {
            'daily': {'start': now - timedelta(days=1), 'end': now},
            'weekly': {'start': now - timedelta(weeks=1), 'end': now},
            'monthly': {'start': now - timedelta(days=30), 'end': now}
        }.get(report_type, {'start': None, 'end': None})

    def generate_report(self, time_range):
        # Simple report content generation
        sales = SalesOrder.objects.filter(
            created_at__range=(time_range['start'], time_range['end'])
        )
        trades = Transaction.objects.filter(
            timestamp__range=(time_range['start'], time_range['end'])
        )

        return {
            'sales': {
                'total': sales.aggregate(total=Sum('total'))['total'] or 0,
                'count': sales.count()
            },
            'trading': {
                'volume': trades.aggregate(total=Sum('quantity'))['total'] or 0,
                'count': trades.count()
            }
        }