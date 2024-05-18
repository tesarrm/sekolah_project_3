from django.shortcuts import render
from rest_framework import viewsets
from .models import Pelanggaran, PelanggaranKategori
from .serializers import PelanggaranSerializer, PelanggaranKategoriSerializer
from user.permissions import IsSuperAdminAndAdminSekolahAndStaffSekolahOrReadOnly
from rest_framework.permissions import IsAuthenticated

class PelanggaranKategoriViewSet(viewsets.ModelViewSet):
    serializer_class = PelanggaranKategoriSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminAndAdminSekolahAndStaffSekolahOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'superadmin'):
            return PelanggaranKategori.objects.all()
        elif hasattr(user, 'adminsekolah'):
            return PelanggaranKategori.objects.filter(sekolah=user.adminsekolah.sekolah)
        elif hasattr(user, 'staffsekolah'):
            return PelanggaranKategori.objects.filter(sekolah=user.staffsekolah.sekolah)
        elif hasattr(user, 'siswa'):
            return PelanggaranKategori.objects.filter(sekolah=user.siswa.sekolah)
        elif hasattr(user, 'orangtua'):
            return PelanggaranKategori.objects.filter(sekolah=user.orangtua.siswa.sekolah)
        else:
            return PelanggaranKategori.objects.none()

class PelanggaranViewSet(viewsets.ModelViewSet):
    serializer_class = PelanggaranSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminAndAdminSekolahAndStaffSekolahOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'superadmin'):
            return Pelanggaran.objects.all()
        elif hasattr(user, 'adminsekolah'):
            return Pelanggaran.objects.filter(sekolah=user.adminsekolah.sekolah)
        elif hasattr(user, 'staffsekolah'):
            return Pelanggaran.objects.filter(sekolah=user.staffsekolah.sekolah)
        elif hasattr(user, 'siswa'):
            return Pelanggaran.objects.filter(sekolah=user.siswa.sekolah)
        elif hasattr(user, 'orangtua'):
            return Pelanggaran.objects.filter(sekolah=user.orangtua.siswa.sekolah)
        else:
            return Pelanggaran.objects.none()
