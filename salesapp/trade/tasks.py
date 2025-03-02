from celery import shared_task
from django.core.mail import send_mail

@shared_task
def notify_trade_execution(order_id):
    from .models import Order
    order = Order.objects.get(id=order_id)
    if order.status == 'executed':
        send_mail(
            'Trade Executed',
            f'Your {order.order_type} order for {order.quantity} {order.product.name} at ${order.price} has been executed.',
            'from@example.com',
            [order.user.email],
            fail_silently=False,
        )