from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, GenreViewSet, BookViewSet

router = DefaultRouter()
router.register('authors', AuthorViewSet)
router.register('genres', GenreViewSet)
router.register('', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
]