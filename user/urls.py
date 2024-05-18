from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, AdminSekolahViewSet, 
    StaffSekolahViewSet, SiswaViewSet, OrangTuaViewSet,
    LoginView, UserDetailView,
    LogoutView,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
# router.register(r'superadmins', SuperAdminViewSet)
router.register(r'adminsekolah', AdminSekolahViewSet)
router.register(r'staffsekolah', StaffSekolahViewSet)
router.register(r'siswa', SiswaViewSet)
router.register(r'orangtua', OrangTuaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', UserDetailView.as_view(), name='me'),
    # path('register/superadmin/', SuperAdminRegisterView.as_view(), name='register-superadmin'),
    # path('register/adminsekolah/', AdminSekolahRegisterView.as_view(), name='register-adminsekolah'),
    # path('register/staffsekolah/', StaffSekolahRegisterView.as_view(), name='register-staffsekolah'),
    # path('register/siswa/', SiswaRegisterView.as_view(), name='register-siswa'),
    # path('register/orangtua/', OrangTuaRegisterView.as_view(), name='register-orangtua'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
