from rest_framework import viewsets
from .models import Book, Order, Rating
from .serializers import BookSerializer, OrderSerializer, RatingSerializer
from .permissions import IsAdmin, IsOperator, IsUser
from rest_framework.decorators import action
from rest_framework.response import Response

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            self.permission_classes = [IsAdmin]
        return super().get_permissions()

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            self.permission_classes = [IsOperator]
        return super().get_permissions()

    @action(detail=True, methods=['post'], permission_classes=[IsOperator])
    def accept_order(self, request, pk=None):
        order = self.get_object()
        order.return_at = request.data.get('return_at')
        order.save()
        return Response({'status': 'order accepted'})

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsUser ]