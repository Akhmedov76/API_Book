from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import Order
from .serializers import OrderSerializer
from users.permissions import IsAdmin, IsOperator, IsUser


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.user.role == 'user':
            return Order.objects.filter(user=self.request.user)
        return Order.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'reserve']:
            permission_classes = [IsUser]
        elif self.action in ['update', 'partial_update', 'process']:
            permission_classes = [IsOperator | IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def reserve(self, request, pk=None):
        order = self.get_object()
        if order.status != Order.PENDING:
            return Response(
                {'error': 'Order can only be reserved when pending'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.start_date = timezone.now()
        order.end_date = order.start_date + timedelta(days=1)
        order.status = Order.ACTIVE
        order.save()

        book = order.book
        book.available -= 1
        book.save()

        return Response(OrderSerializer(order).data)

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        order = self.get_object()
        if order.status != Order.ACTIVE:
            return Response(
                {'error': 'Order must be active to process return'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.return_date = timezone.now()
        order.status = Order.COMPLETED
        order.save()

        book = order.book
        book.available += 1
        book.save()

        return Response(OrderSerializer(order).data)