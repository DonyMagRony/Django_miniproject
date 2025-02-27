from django.utils import timezone
from django.db import models
from django.conf import settings
from product.models import Product

class Order(models.Model):
    ORDER_TYPES = (
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    order_type = models.CharField(max_length=4, choices=ORDER_TYPES, default='buy')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=20,
        choices=(('pending', 'Pending'), ('executed', 'Executed'), ('cancelled', 'Cancelled')),
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order_type} {self.quantity} of {self.product.name} by {self.user.username}"

    class Meta:
        ordering = ['-created_at']

class Transaction(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='transactions',
        null=True,  # Temporarily allow null
        blank=True  # Optional for admin/forms
    )
    executed_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    executed_quantity = models.PositiveIntegerField(default=1)
    executed_at = models.DateTimeField(auto_now_add=True)
    transaction_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Transaction for {self.order} at {self.executed_price}"

    class Meta:
        ordering = ['-executed_at']


class OrderBook(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buy_orders = models.JSONField(default=list)
    sell_orders = models.JSONField(default=list)
    updated_at = models.DateTimeField(auto_now=True)