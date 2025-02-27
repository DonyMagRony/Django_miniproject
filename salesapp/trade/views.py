from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Order, Transaction, OrderBook
from .serializers import OrderSerializer, TransactionSerializer
from product.permissions import TraderOnlyForUnsafe
from rest_framework.renderers import JSONRenderer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .tasks import notify_trade_execution
class OrderViewSet(viewsets.ModelViewSet):
    # ... existing code ...
    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        # Update order book and broadcast
        self.update_order_book(order)
        self.broadcast_order_update(order)

    def update_order_book(self, order):
        order_book, _ = OrderBook.objects.get_or_create(product=order.product)
        if order.order_type == 'buy':
            order_book.buy_orders.append({'id': order.id, 'quantity': order.quantity, 'price': str(order.price)})
        else:
            order_book.sell_orders.append({'id': order.id, 'quantity': order.quantity, 'price': str(order.price)})
        order_book.save()

    def broadcast_order_update(self, order):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"order_book_{order.product.id}",
            {
                'type': 'order_update',
                'order': OrderSerializer(order).data
            }
        )
    def perform_update(self, serializer):
        order = serializer.save()
        if order.status == 'executed':
            notify_trade_execution.delay(order.id)
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, TraderOnlyForUnsafe]
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Transaction.objects.all()
        return Transaction.objects.filter(order__user=self.request.user)