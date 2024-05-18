from django.core.management.base import BaseCommand
from faker import Faker
from akademik.models import Sekolah
from user.models import StaffSekolah, Siswa
from pelanggaran.models import PelanggaranKategori, Pelanggaran

faker = Faker()

class Command(BaseCommand):
    help = 'Generate dummy data for Pelanggaran and PelanggaranKategori models'

    def handle(self, *args, **kwargs):
        self.stdout.write("Generating dummy data for Pelanggaran and PelanggaranKategori models...")

        # Clear existing data
        Pelanggaran.objects.all().delete()
        PelanggaranKategori.objects.all().delete()

        # Create dummy data for PelanggaranKategori
        sekolah_instances = Sekolah.objects.all()
        if not sekolah_instances.exists():
            self.stdout.write(self.style.ERROR('No Sekolah instances found. Please create Sekolah instances first.'))
            return

        for sekolah in sekolah_instances:
            for _ in range(5):
                PelanggaranKategori.objects.create(
                    sekolah=sekolah,
                    nama=faker.word(),
                    poin=faker.random_int(min=1, max=10),
                    catatan=faker.text()
                )

        # Create dummy data for Pelanggaran
        staff_instances = StaffSekolah.objects.all()
        siswa_instances = Siswa.objects.all()
        pelanggaran_kategori_instances = PelanggaranKategori.objects.all()

        if not staff_instances.exists():
            self.stdout.write(self.style.ERROR('No StaffSekolah instances found. Please create StaffSekolah instances first.'))
            return

        if not siswa_instances.exists():
            self.stdout.write(self.style.ERROR('No Siswa instances found. Please create Siswa instances first.'))
            return

        if not pelanggaran_kategori_instances.exists():
            self.stdout.write(self.style.ERROR('No PelanggaranKategori instances found. Please create PelanggaranKategori instances first.'))
            return

        for _ in range(20):
            Pelanggaran.objects.create(
                sekolah=faker.random_element(sekolah_instances),
                staff_sekolah=faker.random_element(staff_instances),
                siswa=faker.random_element(siswa_instances),
                pelanggaran_kategori=faker.random_element(pelanggaran_kategori_instances),
                pesan=faker.text()
            )

        self.stdout.write(self.style.SUCCESS('Successfully generated dummy data for Pelanggaran and PelanggaranKategori models'))
