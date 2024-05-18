from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, AdminSekolahViewSet, 
    StaffSekolahViewSet, SiswaViewSet, OrangTuaViewSet,
    LoginView, UserDetailView,LogoutView,
    # AnakViewSet,
    RegisterAdminSekolahView, TokenNoboxView, AccountListNoboxView
)

router = DefaultRouter()
router.register(r'adminsekolah', AdminSekolahViewSet, basename='adminsekolah')
router.register(r'staffsekolah', StaffSekolahViewSet, basename='staffsekolah')
router.register(r'siswa', SiswaViewSet, basename='siswa')
router.register(r'orangtua', OrangTuaViewSet, basename='orangtua')

urlpatterns = [
    # path('anak/', AnakViewSet.as_view(), name='anak-list'),
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', UserDetailView.as_view(), name='me'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('tokennobox/', TokenNoboxView.as_view(), name='token-nobox'),
    path('accountlistnobox/', AccountListNoboxView.as_view(), name='account-list-nobox'),
    path('register/adminsekolah/', RegisterAdminSekolahView.as_view(), name='register-admin-sekolah'),
]
