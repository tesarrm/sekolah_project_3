from django.db import models
from django.contrib.auth.models import User
from akademik.models import Sekolah

# User
class SuperAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=255)

class AdminSekolah(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sekolah = models.ForeignKey(Sekolah, on_delete=models.CASCADE)
    nama = models.CharField(max_length=255)
    no_telp = models.CharField(max_length=20, blank=True, null=True)

class StaffSekolah(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sekolah = models.ForeignKey(Sekolah, on_delete=models.CASCADE)
    nama = models.CharField(max_length=255)
    jabatan = models.CharField(max_length=255, blank=True, null=True)
    no_telp = models.CharField(max_length=20, blank=True, null=True)

class Siswa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sekolah = models.ForeignKey(Sekolah, on_delete=models.CASCADE)
    nis = models.CharField(max_length=20, unique=True)
    nama = models.CharField(max_length=255)
    kelas = models.CharField(max_length=50)

class OrangTua(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    nama = models.CharField(max_length=255)

