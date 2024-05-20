from django.db import models
from akademik.models import Sekolah
from user.models import StaffSekolah, Siswa 

# Pelanggaran
class PelanggaranKategori(models.Model):
    sekolah = models.ForeignKey(Sekolah, on_delete=models.CASCADE)
    nama = models.CharField(max_length=255)
    poin = models.IntegerField()
    catatan = models.TextField()

    class Meta:
        db_table = 'pelanggaran_kategori'

class Pelanggaran(models.Model):
    sekolah = models.ForeignKey(Sekolah, on_delete=models.CASCADE)
    staff_sekolah = models.ForeignKey(StaffSekolah, on_delete=models.CASCADE)
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    pelanggaran_kategori = models.ForeignKey(PelanggaranKategori, on_delete=models.CASCADE)
    pesan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = 'pelanggaran'
