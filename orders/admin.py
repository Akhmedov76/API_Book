from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'status', 'start_date', 'end_date', 'return_date')
    list_filter = ('status',)
    search_fields = ('user__username', 'book__title')
    readonly_fields = ('created_at',)