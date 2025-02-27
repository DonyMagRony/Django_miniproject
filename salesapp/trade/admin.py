from django.contrib import admin
from .models import Order, Transaction

class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 1
    readonly_fields = ('executed_at',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'order_type', 'quantity', 'price', 'status', 'created_at')
    list_filter = ('order_type', 'status', 'created_at')
    search_fields = ('user__username', 'product__name')
    date_hierarchy = 'created_at'
    inlines = [TransactionInline]
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(user=request.user)
        return qs

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'executed_price', 'executed_quantity', 'transaction_fee', 'executed_at')
    list_filter = ('executed_at',)
    search_fields = ('order__id', 'order__product__name')
    date_hierarchy = 'executed_at'
    readonly_fields = ('executed_at',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(order__user=request.user)
        return qs