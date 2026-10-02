from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BukuViewSet, AnggotaViewSet

router = DefaultRouter()
router.register(r'buku', BukuViewSet)
router.register(r'anggota', AnggotaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]