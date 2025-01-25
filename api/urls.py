from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, OrderViewSet, RatingViewSet

router = DefaultRouter()
router.register('books', BookViewSet)
router.register('orders', OrderViewSet)
router.register('ratings', RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
