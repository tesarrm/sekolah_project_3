from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PelanggaranViewSet, PelanggaranKategoriViewSet

router = DefaultRouter()
router.register(r'pelanggaran_kategori', PelanggaranKategoriViewSet)
router.register(r'pelanggaran', PelanggaranViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
