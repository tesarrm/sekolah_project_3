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
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')

def format_date(date_string):
    date_object = datetime.fromisoformat(date_string)
    formatted_date = date_object.strftime('%A, %d %B %Y')
    return formatted_date


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
    body = """
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                padding: 20px;
            }
            .container {
                background-color: #ffffff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #333333;
                font-size: 24px;
            }
            h2 {
                color: #555555;
                font-size: 20px;
                border-bottom: 2px solid #eeeeee;
                padding-bottom: 5px;
            }
            p {
                color: #666666;
                font-size: 16px;
            }
            .item {
                margin-bottom: 15px;
            }
            .item p {
                margin: 5px 0;
            }
            .bold {
                font-weight: bold;
            }
            .footer {
                margin-top: 20px;
                font-size: 12px;
                color: #999999;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚨 Laporan Pelanggaran 🚨</h1>
    """
    
    for pelanggaran in pelanggaran_data:
        formatted_date = format_date(str(pelanggaran.created_at))
        body += f"""
        <div class="item">
            <h2>📝 Pelanggaran</h2>
            <p><span class="bold">🕒 Waktu:</span> {formatted_date}</p>
            <p><span class="bold">📛 Nama Siswa:</span> {pelanggaran.siswa.nama}</p>
            <p><span class="bold">🏫 Kelas:</span> {pelanggaran.siswa.kelas.tingkat.nama} {pelanggaran.siswa.kelas.jurusan.nama} {pelanggaran.siswa.kelas.nama}</p>
            <p><span class="bold">⚠️ Pelanggaran:</span> {pelanggaran.pelanggaran_kategori.nama}</p>
            <p><span class="bold">📝 Catatan:</span> {pelanggaran.pelanggaran_kategori.catatan}</p>
        </div>
        """
    
    body += """
            <div class="footer">
                <p>Email ini dikirim secara otomatis oleh sistem. Mohon tidak membalas email ini.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    message.attach(MIMEText(body, 'html'))

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

    formatted_date = format_date(str(pelanggaran.created_at))
    body = (
        f"📋 *Laporan Pelanggaran*\n\n"
        f"🕒 *Waktu:* {formatted_date}\n"
        f"👤 *Nama Siswa:* {pelanggaran.siswa.nama}\n"
        f"🏫 *Kelas:*  {pelanggaran.siswa.kelas.tingkat.nama} {pelanggaran.siswa.kelas.jurusan.nama} {pelanggaran.siswa.kelas.nama}\n"
        f"⚠️ *Kategori Pelanggaran:* {pelanggaran.pelanggaran_kategori.nama}\n"
        f"🔍 *Catatan:* {pelanggaran.pelanggaran_kategori.catatan}\n"
    )

    attachment = ""

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
        send_pelanggaran_email(email=pelanggaran.siswa.user.email, pelanggaran_data=[pelanggaran])

        # send nobox
        message_result = send_nobox_message(request, pelanggaran)

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

