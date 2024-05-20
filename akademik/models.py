from django.db import models

# Akademik
class Sekolah(models.Model):
    nama = models.CharField(max_length=255)
    alamat = models.TextField()
    kota = models.CharField(max_length=100, blank=True, null=True)  
    provinsi = models.CharField(max_length=100, blank=True, null=True)  
    no_telp = models.CharField(max_length=20, blank=True, null=True)  
    email = models.EmailField(max_length=254, blank=True, null=True)  
    website = models.URLField(max_length=200, blank=True, null=True)  
    catatan = models.TextField(blank=True, null=True)  

class Tingkat(models.Model):
    nama = models.CharField(max_length=50)
    sekolah = models.ForeignKey(Sekolah, on_delete=models.CASCADE)

class Jurusan(models.Model):
    nama = models.CharField(max_length=50)
    sekolah = models.ForeignKey(Sekolah, on_delete=models.CASCADE)

class Kelas(models.Model):
    nama = models.CharField(max_length=50)
    sekolah = models.ForeignKey(Sekolah, on_delete=models.CASCADE)
    tingkat = models.ForeignKey(Tingkat, on_delete=models.CASCADE)
    jurusan = models.ForeignKey(Jurusan, on_delete=models.CASCADE)