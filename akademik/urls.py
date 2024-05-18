from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SekolahViewSet, TingkatViewSet, JurusanViewSet, KelasViewSet

router = DefaultRouter()
router.register(r'sekolah', SekolahViewSet, basename='sekolah')
router.register(r'tingkat', TingkatViewSet, basename='tingkat')
router.register(r'jurusan', JurusanViewSet, basename='jurusan')
router.register(r'kelas', KelasViewSet, basename='kelas')

urlpatterns = [
    path('', include(router.urls)),
]