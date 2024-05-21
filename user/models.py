from django.db import models
from django.contrib.auth.models import User
from akademik.models import Sekolah, Kelas

# User
class SuperAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=255)

class AdminSekolah(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sekolah = models.ForeignKey(Sekolah, on_delete=models.CASCADE)
    nama = models.CharField(max_length=255)
    no_telp = models.CharField(max_length=20, blank=True, null=True)
    token_nobox = models.TextField(blank=True, null=True)
    account_id_nobox= models.TextField(blank=True, null=True)

class StaffSekolah(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sekolah = models.ForeignKey(Sekolah, on_delete=models.CASCADE)
    nama = models.CharField(max_length=255)
    jabatan = models.CharField(max_length=255, blank=True, null=True)
    no_telp = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True) 
    catatan = models.TextField(blank=True, null=True) 

class OrangTua(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=255)
    no_telp = models.TextField(blank=True, null=True) 

class Siswa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sekolah = models.ForeignKey(Sekolah, on_delete=models.CASCADE)
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)
    nis = models.CharField(max_length=20, unique=True)
    nama = models.CharField(max_length=255)
    orangtua = models.ForeignKey(OrangTua, on_delete=models.CASCADE, blank=True, null=True) 
    catatan = models.TextField(blank=True, null=True) 
