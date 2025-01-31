from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    fine_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('user', 'fine_amount', 'total_amount')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['fine_amount'] = instance.calculate_fine()
        representation['total_amount'] = instance.calculate_total()
        return representation