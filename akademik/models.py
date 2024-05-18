from django.db import models

# Akademik
class Sekolah(models.Model):
    nama = models.CharField(max_length=255)
    alamat = models.TextField()

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

