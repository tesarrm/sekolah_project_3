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
    AdminSekolahRegisterSerializer
)
from .permissions import (
    IsSuperAdminOrReadOnly, IsAdminSekolahOrReadOnly, 
    IsStaffSekolahOrReadOnly, IsSiswaOrReadOnly, IsOrangTuaOrReadOnly,
    IsSuperAdmin, IsAdminSekolah, IsStaffSekolah, IsSiswa, IsOrangTua
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
    queryset = AdminSekolah.objects.all()
    serializer_class = AdminSekolahSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrReadOnly]

class StaffSekolahViewSet(viewsets.ModelViewSet):
    queryset = StaffSekolah.objects.all()
    serializer_class = StaffSekolahSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrReadOnly, IsAdminSekolahOrReadOnly]

class SiswaViewSet(viewsets.ModelViewSet):
    queryset = Siswa.objects.all()
    serializer_class = SiswaSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrReadOnly, IsAdminSekolahOrReadOnly, IsStaffSekolahOrReadOnly]

class OrangTuaViewSet(viewsets.ModelViewSet):
    queryset = OrangTua.objects.all()
    serializer_class = OrangTuaSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrReadOnly, IsAdminSekolahOrReadOnly, IsStaffSekolahOrReadOnly]


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


## Register

# class SuperAdminRegisterView(generics.CreateAPIView):
#     queryset = SuperAdmin.objects.all()
#     serializer_class = SuperAdminRegisterSerializer

class AdminSekolahRegisterView(generics.CreateAPIView):
    queryset = AdminSekolah.objects.all()
    serializer_class = AdminSekolahRegisterSerializer

# class StaffSekolahRegisterView(generics.CreateAPIView):
#     queryset = StaffSekolah.objects.all()
#     serializer_class = StaffSekolahRegisterSerializer

# class SiswaRegisterView(generics.CreateAPIView):
#     queryset = Siswa.objects.all()
#     serializer_class = SiswaRegisterSerializer

# class OrangTuaRegisterView(generics.CreateAPIView):
#     queryset = OrangTua.objects.all()
#     serializer_class = OrangTuaRegisterSerializer


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