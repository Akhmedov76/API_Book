from rest_framework import serializers
from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ('user',)