from django.contrib import admin
from .models import SalesOrder, OrderItem, Invoice

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('subtotal',)

@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'sales_rep', 'customer', 'status', 'discount', 'total', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('sales_rep__username', 'customer__username')
    date_hierarchy = 'created_at'
    inlines = [OrderItemInline]
    readonly_fields = ('created_at', 'updated_at', 'total')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            if request.user.role == 'seller':
                return qs.filter(sales_rep=request.user)
            return qs.filter(customer=request.user)
        return qs

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price', 'subtotal')
    list_filter = ('order__status',)
    search_fields = ('order__id', 'product__name')
    readonly_fields = ('subtotal',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'total_amount', 'generated_at', 'due_date', 'paid')
    list_filter = ('paid', 'generated_at', 'due_date')
    search_fields = ('order__id',)
    date_hierarchy = 'generated_at'
    readonly_fields = ('generated_at', 'total_amount')
    actions = ['mark_as_paid']

    def mark_as_paid(self, request, queryset):
        queryset.update(paid=True)
        self.message_user(request, "Selected invoices marked as paid.")
    mark_as_paid.short_description = "Mark selected invoices as paid"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            if request.user.role == 'seller':
                return qs.filter(order__sales_rep=request.user)
            return qs.filter(order__customer=request.user)
        return qs