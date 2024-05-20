from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Pelanggaran, PelanggaranKategori
from .serializers import PelanggaranSerializer, PelanggaranKategoriSerializer, PelanggaranNestedSerializer
from user.permissions import IsSuperAdminAndAdminSekolahAndStaffSekolahOrReadOnly
from rest_framework.permissions import IsAuthenticated
from user.nobox.nobox import Nobox 
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.decorators import action

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
    serializer_class = PelanggaranNestedSerializer
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

    def create(self, request, *args, **kwargs):
        # Buat objek pelanggaran
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        token_nobox = request.data.get('token_nobox')
        resextId = request.data.get('extId')
        resaccountId= request.data.get('accountId')
        resbody = request.data.get('body')

        nobox = Nobox(token_nobox)

        print(token_nobox)

        extId = resextId # nomor tujuan
        channelId = "1" # 1
        accountIds = resaccountId # 546785296764933
        bodyType = "1" # 1 = text
        body = resbody # isi
        attachment = ""

        # Kirim pesan menggunakan Nobox
        message_result = nobox.sendInboxMessageExt(
            extId, 
            channelId, 
            accountIds, 
            bodyType, 
            body, 
            attachment
        )

        if message_result['IsError']:
            return Response({
                'error': 'Failed to send message', 
                'details': message_result['Error']}, 
                status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PelanggaranSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=['get'], url_path='today')
    def get_today_pelanggaran(self, request):
        today = timezone.now().date()
        user = self.request.user
        
        if hasattr(user, 'superadmin'):
            queryset = Pelanggaran.objects.filter(created_at__date=today)
        elif hasattr(user, 'adminsekolah'):
            queryset = Pelanggaran.objects.filter(sekolah=user.adminsekolah.sekolah, created_at__date=today)
        elif hasattr(user, 'staffsekolah'):
            queryset = Pelanggaran.objects.filter(sekolah=user.staffsekolah.sekolah, created_at__date=today)
        elif hasattr(user, 'siswa'):
            queryset = Pelanggaran.objects.filter(sekolah=user.siswa.sekolah, created_at__date=today)
        elif hasattr(user, 'orangtua'):
            queryset = Pelanggaran.objects.filter(sekolah=user.orangtua.siswa.sekolah, created_at__date=today)
        else:
            queryset = Pelanggaran.objects.none()
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-kelas/(?P<kelas_id>\d+)')
    def get_by_kelas(self, request, kelas_id=None):
        pelanggaran = Pelanggaran.objects.filter(siswa__kelas__id=kelas_id)
        serializer = self.get_serializer(pelanggaran, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='detail/(?P<kelas_id>\d+)/(?P<pelanggaran_id>\d+)')
    def detail_by_kelas(self, request, pk=None, kelas_id=None, pelanggaran_id=None):
        print(kelas_id)
        print(pelanggaran_id)
        try:
            pelanggaran = Pelanggaran.objects.get(id=pelanggaran_id, siswa__kelas__id=kelas_id)
        except Pelanggaran.DoesNotExist:
            return Response({'error': 'Pelanggaran not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(pelanggaran)
        return Response(serializer.data)
