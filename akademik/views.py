from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Sekolah, Tingkat, Jurusan, Kelas
from .serializers import SekolahSerializer, TingkatSerializer, JurusanSerializer, KelasSerializer
from user.permissions import IsSuperAdminOrReadOnly, IsSuperAdminAndAdminSekolahAndStaffSekolahOrReadOnly

class SekolahViewSet(viewsets.ModelViewSet):
    queryset = Sekolah.objects.all()
    serializer_class = SekolahSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrReadOnly]

class TingkatViewSet(viewsets.ModelViewSet):
    serializer_class = TingkatSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminAndAdminSekolahAndStaffSekolahOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'superadmin'):
            return Tingkat.objects.all()
        elif hasattr(user, 'adminsekolah'):
            return Tingkat.objects.filter(sekolah=user.adminsekolah.sekolah)
        elif hasattr(user, 'staffsekolah'):
            return Tingkat.objects.filter(sekolah=user.staffsekolah.sekolah)
        elif hasattr(user, 'siswa'):
            return Tingkat.objects.filter(sekolah=user.siswa.sekolah)
        elif hasattr(user, 'orangtua'):
            return OrangTua.objects.filter(sekolah=user.orangtua.siswa.sekolah)
        else:
            return AdminSekolah.objects.none()

class JurusanViewSet(viewsets.ModelViewSet):
    serializer_class = JurusanSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminAndAdminSekolahAndStaffSekolahOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'superadmin'):
            return Jurusan.objects.all()
        elif hasattr(user, 'adminsekolah'):
            return Jurusan.objects.filter(sekolah=user.adminsekolah.sekolah)
        elif hasattr(user, 'staffsekolah'):
            return Jurusan.objects.filter(sekolah=user.staffsekolah.sekolah)
        elif hasattr(user, 'siswa'):
            return Jurusan.objects.filter(sekolah=user.siswa.sekolah)
        elif hasattr(user, 'orangtua'):
            return OrangTua.objects.filter(sekolah=user.orangtua.siswa.sekolah)
        else:
            return AdminSekolah.objects.none()

class KelasViewSet(viewsets.ModelViewSet):
    serializer_class = KelasSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminAndAdminSekolahAndStaffSekolahOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'superadmin'):
            return Kelas.objects.all()
        elif hasattr(user, 'adminsekolah'):
            return Kelas.objects.filter(sekolah=user.adminsekolah.sekolah)
        elif hasattr(user, 'staffsekolah'):
            return Kelas.objects.filter(sekolah=user.staffsekolah.sekolah)
        elif hasattr(user, 'siswa'):
            return Kelas.objects.filter(sekolah=user.siswa.sekolah)
        elif hasattr(user, 'orangtua'):
            return OrangTua.objects.filter(sekolah=user.orangtua.siswa.sekolah)
        else:
            return AdminSekolah.objects.none()
