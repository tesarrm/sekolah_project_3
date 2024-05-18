from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, AdminSekolahViewSet, 
    StaffSekolahViewSet, SiswaViewSet, OrangTuaViewSet,
    LoginView, UserDetailView,
    LogoutView,
    AnakViewSet
)

router = DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'superadmins', SuperAdminViewSet)
# router.register(r'adminsekolah', AdminSekolahViewSet)
# router.register(r'staffsekolah', StaffSekolahViewSet)
# router.register(r'siswa', SiswaViewSet)
# router.register(r'orangtua', OrangTuaViewSet)
router.register(r'adminsekolah', AdminSekolahViewSet, basename='adminsekolah')
router.register(r'staffsekolah', StaffSekolahViewSet, basename='staffsekolah')
router.register(r'siswa', SiswaViewSet, basename='siswa')
router.register(r'orangtua', OrangTuaViewSet, basename='orangtua')

urlpatterns = [
    path('anak/', AnakViewSet.as_view(), name='anak-list'),
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', UserDetailView.as_view(), name='me'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
