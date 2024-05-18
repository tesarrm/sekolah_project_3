from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, SuperAdminViewSet, AdminSekolahViewSet, 
    StaffSekolahViewSet, SiswaViewSet, OrangTuaViewSet,
    LoginView
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'superadmins', SuperAdminViewSet)
router.register(r'adminsekolah', AdminSekolahViewSet)
router.register(r'staffsekolah', StaffSekolahViewSet)
router.register(r'siswa', SiswaViewSet)
router.register(r'orangtua', OrangTuaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
]
