from django.db import models
from django.utils import timezone
from users.models import CustomUser
from books.models import Book
from decimal import Decimal


class Order(models.Model):
    PENDING = 'pending'
    ACTIVE = 'active'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACTIVE, 'Active'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_fine(self):
        if not self.return_date or not self.end_date or self.status != self.COMPLETED:
            return 0

        if self.return_date <= self.end_date:
            return 0

        days_late = (self.return_date - self.end_date).days
        daily_fine = self.book.daily_price * Decimal('0.01')  # 1% of daily price
        return days_late * daily_fine

    def calculate_total(self):
        if not self.start_date or not self.return_date:
            return 0

        days_used = (self.return_date - self.start_date).days or 1
        rental_cost = days_used * self.book.daily_price
        fine = self.calculate_fine()
        return rental_cost + fine

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"