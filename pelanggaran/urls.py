from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PelanggaranViewSet, PelanggaranKategoriViewSet

router = DefaultRouter()
router.register(r'pelanggaran_kategori', PelanggaranKategoriViewSet, basename='pelanggaran_kategori')
router.register(r'pelanggaran', PelanggaranViewSet, basename='pelanggaran')

urlpatterns = [
    path('', include(router.urls)),
]
