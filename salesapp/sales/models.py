from django.db import models
from django.utils import timezone
from userManagement.models import CustomUser
from product.models import Product

class SalesOrder(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('APPROVED', 'Approved'),
        ('SHIPPED', 'Shipped'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    sales_rep = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name='sales_orders_managed'
    )
    customer = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name='sales_orders'
    )
    products = models.ManyToManyField(Product, through='OrderItem')
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='DRAFT')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Order {self.id} by {self.customer.username} (Rep: {self.sales_rep.username})"

    @property
    def total(self):
        item_total = sum(item.subtotal for item in self.orderitem_set.all())
        return item_total * (1 - self.discount/100)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if hasattr(self, 'invoice'):
            self.invoice.total_amount = self.total
            self.invoice.save()

    class Meta:
        ordering = ['-created_at']

class OrderItem(models.Model):
    order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)  # Default added
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Default added

    @property
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"

class Invoice(models.Model):
    order = models.OneToOneField(
        SalesOrder,
        on_delete=models.CASCADE,
        related_name='invoice'
    )
    pdf_file = models.FileField(upload_to='invoices/', null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    generated_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(default=timezone.now)
    paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk and not self.total_amount:
            self.total_amount = self.order.total  # Remove ()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice for Order {self.order.id}"

    class Meta:
        ordering = ['-generated_at']