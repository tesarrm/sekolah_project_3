from rest_framework import viewsets, views, status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import SuperAdmin, AdminSekolah, StaffSekolah, Siswa, OrangTua
from .serializers import (
    UserSerializer, SuperAdminSerializer, AdminSekolahSerializer, 
    StaffSekolahSerializer, SiswaSerializer, OrangTuaSerializer,
    LoginSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class SuperAdminViewSet(viewsets.ModelViewSet):
    queryset = SuperAdmin.objects.all()
    serializer_class = SuperAdminSerializer
    permission_classes = [IsAuthenticated]

class AdminSekolahViewSet(viewsets.ModelViewSet):
    queryset = AdminSekolah.objects.all()
    serializer_class = AdminSekolahSerializer
    permission_classes = [IsAuthenticated]

class StaffSekolahViewSet(viewsets.ModelViewSet):
    queryset = StaffSekolah.objects.all()
    serializer_class = StaffSekolahSerializer
    permission_classes = [IsAuthenticated]

class SiswaViewSet(viewsets.ModelViewSet):
    queryset = Siswa.objects.all()
    serializer_class = SiswaSerializer
    permission_classes = [IsAuthenticated]

class OrangTuaViewSet(viewsets.ModelViewSet):
    queryset = OrangTua.objects.all()
    serializer_class = OrangTuaSerializer
    permission_classes = [IsAuthenticated]

# Authentication

class LoginView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)