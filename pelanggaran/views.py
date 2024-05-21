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
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from rest_framework import status
from django.forms.models import model_to_dict
import json

# def send_pelanggaran_email(email, pelanggaran_data):
#     smtp_server = 'smtp.gmail.com'
#     smtp_port = 587
#     sender_email = 'tesarrm58@gmail.com'
#     password = 'cslulirpurnvnnpw'

#     message = MIMEMultipart()
#     message['From'] = sender_email
#     message['To'] = email
#     message['Subject'] = 'Laporan Pelanggaran'

#     # Membuat isi email berdasarkan data pelanggaran
#     body = "Berikut adalah laporan pelanggaran:\n\n"
#     for pelanggaran in pelanggaran_data:
#         body += f"- ID Pelanggaran: {pelanggaran.id}\n"
#         body += f"  Waktu: {pelanggaran.created_at}\n"
#         body += f"  Nama Siswa: {pelanggaran.siswa.nama}\n"
#         body += f"  Kelas: {pelanggaran.siswa.kelas.nama}\n"
#         body += f"  Deskripsi: {pelanggaran.deskripsi}\n\n"

#     message.attach(MIMEText(body, 'plain'))

#     try:
#         server = smtplib.SMTP(smtp_server, smtp_port)
#         server.starttls()
#         server.login(sender_email, password)
#         text = message.as_string()
#         server.sendmail(sender_email, email, text)
#         server.quit()

#         return Response({'message': 'Email sent successfully'}, status=status.HTTP_200_OK)
#     except Exception as e:
#         print(e)
#         return Response({'error': 'Failed to send email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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

def send_pelanggaran_email(email, pelanggaran_data):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'tesarrm58@gmail.com'
    password = 'cslulirpurnvnnpw'

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email
    message['Subject'] = 'Laporan Pelanggaran'

    # Membuat isi email berdasarkan data pelanggaran
    body = "Berikut adalah laporan pelanggaran:\n\n"
    for pelanggaran in pelanggaran_data:
        body += f"  Waktu: {pelanggaran.created_at}\n"
        body += f"  Nama Siswa: {pelanggaran.siswa.nama}\n"
        body += f"  Kelas: {pelanggaran.siswa.kelas.nama}\n"
        # body += f"  Deskripsi: {pelanggaran.deskripsi}\n\n"

    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)
        text = message.as_string()
        server.sendmail(sender_email, email, text)
        server.quit()

        return Response({'message': 'Email sent successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'error': 'Failed to send email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def send_nobox_message(request, pelanggaran):
    token_nobox = request.data.get('token_nobox')
    nobox = Nobox(token_nobox)
    extId = pelanggaran.siswa.orangtua.no_telp
    channelId = "1"

    sekolah = pelanggaran.sekolah
    adminsekolah = sekolah.adminsekolah_set.first()
    if not adminsekolah:
        return {'IsError': True, 'Error': 'No adminsekolah found for the given school'}

    accountIds = adminsekolah.account_id_nobox
    bodyType = "1"
    body = f"Berikut adalah laporan pelanggaran:\n\nWaktu: {pelanggaran.created_at}\nNama Siswa: {pelanggaran.siswa.nama}\nKelas: {pelanggaran.siswa.kelas.nama}\n"
    attachment = ""

    message_result = nobox.sendInboxMessageExt(
        extId,
        channelId,
        accountIds,
        bodyType,
        body,
        attachment
    )

    return message_result

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

    def get_serializer_class(self):
        if self.action == 'create':
            return PelanggaranSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        user = self.request.user

        if hasattr(user, 'siswa') or hasattr(user, 'orangtua'):
            return Response({'error': 'Only staff can create pelanggaran'}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()

        if hasattr(user, 'superadmin'):
            data['staff_sekolah'] = user.superadmin.id
            data['sekolah'] = user.superadmin.sekolah.id
        if hasattr(user, 'adminsekolah'):
            data['staff_sekolah'] = user.adminsekolah.id
            data['sekolah'] = user.adminsekolah.sekolah.id
        if hasattr(user, 'staffsekolah'):
            data['staff_sekolah'] = user.staffsekolah.id
            data['sekolah'] = user.staffsekolah.sekolah.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        pelanggaran = serializer.save()

        # send email
        send_pelanggaran_email(email="tesarrm58@gmail.com", pelanggaran_data=[pelanggaran])

        # send nobox
        message_result = send_nobox_message(request, pelanggaran)

        if message_result['IsError']:
            return Response({
                'error': 'Failed to send message', 
                'details': message_result['Error']}, 
                status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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

