from rest_framework import viewsets, views, status, generics 
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.models import User
from .models import SuperAdmin, AdminSekolah, StaffSekolah, Siswa, OrangTua
from .serializers import (
    UserSerializer, AdminSekolahSerializer, 
    StaffSekolahSerializer, SiswaSerializer, OrangTuaSerializer,
    LoginSerializer,
    SuperAdminDetailSerializer, AdminSekolahDetailSerializer, 
    StaffSekolahDetailSerializer, SiswaDetailSerializer, OrangTuaDetailSerializer,
)
from .permissions import (
    IsSuperAdminOrReadOnly, IsAdminSekolahOrReadOnly, 
    IsStaffSekolahOrReadOnly, IsSiswaOrReadOnly, IsOrangTuaOrReadOnly,
    IsSuperAdmin, IsAdminSekolah, IsStaffSekolah, IsSiswa, IsOrangTua,
    IsSuperAdminAndAdminSekolahOrReadOnly, IsSuperAdminAndAdminSekolahAndStaffSekolahOrReadOnly
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

# class SuperAdminViewSet(viewsets.ModelViewSet):
#     queryset = SuperAdmin.objects.all()
#     serializer_class = SuperAdminSerializer
#     permission_classes = [IsAuthenticated, IsSuperAdminOrReadOnly]

class AdminSekolahViewSet(viewsets.ModelViewSet):
    serializer_class = AdminSekolahSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'superadmin'):
            return AdminSekolah.objects.all()
        elif hasattr(user, 'adminsekolah'):
            return AdminSekolah.objects.filter(sekolah=user.adminsekolah.sekolah)
        elif hasattr(user, 'staffsekolah'):
            return AdminSekolah.objects.filter(sekolah=user.staffsekolah.sekolah)
        elif hasattr(user, 'siswa'):
            return AdminSekolah.objects.filter(sekolah=user.siswa.sekolah)
        elif hasattr(user, 'orangtua'):
            return OrangTua.objects.filter(sekolah=user.orangtua.siswa.sekolah)
        else:
            return AdminSekolah.objects.none()

class StaffSekolahViewSet(viewsets.ModelViewSet):
    serializer_class = StaffSekolahSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminAndAdminSekolahOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'superadmin'):
            return StaffSekolah.objects.all()
        elif hasattr(user, 'adminsekolah'):
            return StaffSekolah.objects.filter(sekolah=user.adminsekolah.sekolah)
        elif hasattr(user, 'staffsekolah'):
            return StaffSekolah.objects.filter(sekolah=user.staffsekolah.sekolah)
        elif hasattr(user, 'siswa'):
            return StaffSekolah.objects.filter(sekolah=user.siswa.sekolah)
        elif hasattr(user, 'orangtua'):
            return OrangTua.objects.filter(sekolah=user.orangtua.siswa.sekolah)
        else:
            return StaffSekolah.objects.none()

class SiswaViewSet(viewsets.ModelViewSet):
    serializer_class = SiswaSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminAndAdminSekolahAndStaffSekolahOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'superadmin'):
            return Siswa.objects.all()
        elif hasattr(user, 'adminsekolah'):
            return Siswa.objects.filter(sekolah=user.adminsekolah.sekolah)
        elif hasattr(user, 'staffsekolah'):
            return Siswa.objects.filter(sekolah=user.staffsekolah.sekolah)
        elif hasattr(user, 'siswa'):
            return Siswa.objects.filter(sekolah=user.siswa.sekolah)
        elif hasattr(user, 'orangtua'):
            return OrangTua.objects.filter(sekolah=user.orangtua.siswa.sekolah)
        else:
            return Siswa.objects.none()

class OrangTuaViewSet(viewsets.ModelViewSet):
    serializer_class = OrangTuaSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminAndAdminSekolahAndStaffSekolahOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'superadmin'):
            return OrangTua.objects.all()
        elif hasattr(user, 'adminsekolah'):
            return OrangTua.objects.filter(siswa__sekolah=user.adminsekolah.sekolah)
        elif hasattr(user, 'staffsekolah'):
            return OrangTua.objects.filter(siswa__sekolah=user.staffsekolah.sekolah)
        elif hasattr(user, 'siswa'):
            return OrangTua.objects.filter(siswa__sekolah=user.siswa.sekolah)
        elif hasattr(user, 'orangtua'):
            return OrangTua.objects.filter(siswa__sekolah=user.orangtua.siswa.sekolah)
        else:
            return OrangTua.objects.none()

class AnakViewSet(APIView):
    def get(self, request):
        user = request.user
        try:
            # Ambil orang tua berdasarkan user yang terautentikasi
            orang_tua = OrangTua.objects.get(user=user)
            # Ambil semua siswa yang terkait dengan orang tua tersebut
            anak_anak = orang_tua.siswa.all()
            # Serialize data siswa
            serializer = SiswaSerializer(anak_anak, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except OrangTua.DoesNotExist:
            return Response({"message": "Orang tua tidak ditemukan"}, status=status.HTTP_404_NOT_FOUND)

# Authentication

## Login

class LoginView(views.APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)

## User detail current login

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if hasattr(user, 'superadmin'):
            serializer = SuperAdminDetailSerializer(user.superadmin)
        elif hasattr(user, 'adminsekolah'):
            serializer = AdminSekolahDetailSerializer(user.adminsekolah)
        elif hasattr(user, 'staffsekolah'):
            serializer = StaffSekolahDetailSerializer(user.staffsekolah)
        elif hasattr(user, 'siswa'):
            serializer = SiswaDetailSerializer(user.siswa)
        elif hasattr(user, 'orangtua'):
            serializer = OrangTuaDetailSerializer(user.orangtua)
        else:
            return Response({'detail': 'User type not recognized'}, status=400)

        return Response(serializer.data)

## Logout

class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Hapus token pengguna saat ini
            request.user.auth_token.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AttributeError:
            return Response(status=status.HTTP_400_BAD_REQUEST)