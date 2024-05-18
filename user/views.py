from rest_framework import viewsets, views, status, generics 
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .nobox.nobox import Nobox 
from django.contrib.auth import authenticate

from django.contrib.auth.models import User
from .models import SuperAdmin, AdminSekolah, StaffSekolah, Siswa, OrangTua
from .serializers import (
    UserSerializer, AdminSekolahSerializer, 
    StaffSekolahSerializer, SiswaSerializer, OrangTuaSerializer,
    LoginSerializer,
    SuperAdminDetailSerializer, AdminSekolahDetailSerializer, 
    StaffSekolahDetailSerializer, SiswaDetailSerializer, OrangTuaDetailSerializer,
    AdminSekolahRegistrationSerializer 
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

# Registrasi

class TokenNoboxView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        # Generate token dari Nobox
        username = request.data.get('username')
        password = request.data.get('password')

        nobox = Nobox()
        nobox_result = nobox.generateToken(username, password)

        if nobox_result['IsError']:
            return Response({'error': 'Failed to generate Nobox token', 'details': nobox_result['Error']}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'nobox_token': nobox_result['Data']
        }, status=status.HTTP_200_OK)

class RegisterAdminSekolahView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = AdminSekolahRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login

# class LoginView(views.APIView):
#     permission_classes = [AllowAny]
#     def post(self, request, *args, **kwargs):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key}, status=status.HTTP_200_OK)

# class LoginView(views.APIView):
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         # Autentikasi pengguna
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)

#         # Generate token dari Nobox
#         username = request.data.get('username')
#         password = request.data.get('password')
        
#         if hasattr(user, 'superadmin') and user.superadmin: 
#             # Superadmin tidak memerlukan token Nobox
#             return Response({
#                 'token': token.key,
#                 'message': 'Superadmin access granted without Nobox token'
#             }, status=status.HTTP_200_OK)
#         else:
#             nobox = Nobox()
#             nobox_result = nobox.generateToken(username, password)

#         # Periksa apakah ada kesalahan saat generate token dari Nobox
#         if nobox_result['IsError']:
#             return Response({'error': 'Failed to generate Nobox token', 'details': nobox_result['Error']}, status=status.HTTP_400_BAD_REQUEST)

#         # Sertakan token dari Nobox dalam respon
#         return Response({
#             'token': token.key,
#             'nobox_token': nobox_result['Data']
#         }, status=status.HTTP_200_OK)

## sekaligus simpan ke atribut token_nbobx

class LoginView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Autentikasi pengguna
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        # Generate token dari Nobox
        username = request.data.get('username')
        password = request.data.get('password')
        
        if hasattr(user, 'superadmin') and user.superadmin:
            # Superadmin tidak memerlukan token Nobox
            return Response({
                'token': token.key,
                'message': 'Superadmin access granted without Nobox token'
            }, status=status.HTTP_200_OK)
        else:
            nobox = Nobox()
            nobox_result = nobox.generateToken(username, password)

        # Periksa apakah ada kesalahan saat generate token dari Nobox
        if nobox_result['IsError']:
            return Response({'error': 'Failed to generate Nobox token', 'details': nobox_result['Error']}, status=status.HTTP_400_BAD_REQUEST)

        nobox_token = nobox_result['Data']
        
        # Simpan token_nobox ke atribut admin_sekolah
        if hasattr(user, 'adminsekolah'):
            admin_sekolah = user.adminsekolah
            admin_sekolah.token_nobox = nobox_token
            admin_sekolah.save()
        
        # Sertakan token dari Nobox dalam respon
        return Response({
            'token': token.key,
            'nobox_token': nobox_token
        }, status=status.HTTP_200_OK)

# class LoginView(views.APIView):
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         # Ambil email dan password dari permintaan
#         username = request.data.get('username')
#         password = request.data.get('password')

#         # Cek apakah pengguna dengan email ini ada
#         try:
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             # Jika pengguna tidak ada, buat akun baru
#             user = User.objects.create_user(username=username, email=username, password=password)

#         # Autentikasi pengguna
#         user = authenticate(request=request, username=user.username, password=password)
#         if not user:
#             return Response({'error': 'Invalid login credentials.'}, status=status.HTTP_400_BAD_REQUEST)

#         token, created = Token.objects.get_or_create(user=user)

#         # Generate token dari Nobox
#         nobox = Nobox()
#         nobox_result = nobox.generateToken(username, password)

#         # Periksa apakah ada kesalahan saat generate token dari Nobox
#         if nobox_result['IsError']:
#             return Response({'error': 'Failed to generate Nobox token', 'details': nobox_result['Error']}, status=status.HTTP_400_BAD_REQUEST)

#         # Sertakan token dari Nobox dalam respon
#         return Response({
#             'token': token.key,
#             'nobox_token': nobox_result['Data']
#         }, status=status.HTTP_200_OK)

# class LoginView(views.APIView):
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         # Ambil email atau username dan password dari permintaan
#         identifier = serializer.validated_data['identifier']
#         password = serializer.validated_data['password']

#         # Cek apakah pengguna login dengan email atau username
#         if '@' in identifier:
#             email = identifier
#             try:
#                 user = User.objects.get(email=email)
#             except User.DoesNotExist:
#                 # Jika pengguna tidak ada, buat akun baru
#                 user = User.objects.create_user(username=email, email=email, password=password)
#         else:
#             username = identifier
#             try:
#                 user = User.objects.get(username=username)
#                 email = user.email
#             except User.DoesNotExist:
#                 return Response({'error': 'Invalid login credentials.'}, status=status.HTTP_400_BAD_REQUEST)

#         # Autentikasi pengguna
#         user = authenticate(request=request, username=user.username, password=password)
#         if not user:
#             return Response({'error': 'Invalid login credentials.'}, status=status.HTTP_400_BAD_REQUEST)

#         token, created = Token.objects.get_or_create(user=user)

#         # Cek apakah pengguna adalah superadmin
#         if hasattr(user, 'superadmin') and user.superadmin:
#             # Superadmin tidak memerlukan token Nobox
#             return Response({
#                 'token': token.key,
#                 'message': 'Superadmin access granted without Nobox token'
#             }, status=status.HTTP_200_OK)
#         else:
#             # Generate token dari Nobox
#             nobox = Nobox()
#             nobox_result = nobox.generateToken(email, password)

#             # Periksa apakah ada kesalahan saat generate token dari Nobox
#             if nobox_result['IsError']:
#                 return Response({'error': 'Failed to generate Nobox token', 'details': nobox_result['Error']}, status=status.HTTP_400_BAD_REQUEST)

#             # Sertakan token dari Nobox dalam respon
#             return Response({
#                 'token': token.key,
#                 'nobox_token': nobox_result['Data']
#             }, status=status.HTTP_200_OK)

# User detail current login

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

# Logout

class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Hapus token pengguna saat ini
            request.user.auth_token.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AttributeError:
            return Response(status=status.HTTP_400_BAD_REQUEST)