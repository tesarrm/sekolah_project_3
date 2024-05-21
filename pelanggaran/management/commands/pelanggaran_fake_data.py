from django.core.management.base import BaseCommand
from faker import Faker
from akademik.models import Sekolah
from user.models import StaffSekolah, Siswa
from pelanggaran.models import PelanggaranKategori, Pelanggaran

faker = Faker()

class Command(BaseCommand):
    help = 'Generate dummy data for the application'

    def handle(self, *args, **kwargs):
        self.stdout.write("Generating dummy data...")

        # Clear existing data
        Pelanggaran.objects.all().delete()
        PelanggaranKategori.objects.all().delete()

        # Create dummy data for PelanggaranKategori
        sekolah_instances = Sekolah.objects.all()
        if not sekolah_instances.exists():
            self.stdout.write(self.style.ERROR('No Sekolah instances found. Please create Sekolah instances first.'))
            return

        for sekolah in sekolah_instances:
            pelanggaran_kategori_list= []
            for pelanggaran_kategori_name in ['Merokok', 'Bolos', 'Mabuk', 'Bertengkar', 'Narkoba']:
                pelanggaran_kategori = PelanggaranKategori.objects.create(
                    sekolah=sekolah,
                    nama=pelanggaran_kategori_name,
                    poin=faker.random_int(min=1, max=10),
                    catatan=faker.text()
                )
                pelanggaran_kategori_list.append(pelanggaran_kategori)

            # Filter staff and siswa based on the current school
            staff_instances = StaffSekolah.objects.filter(sekolah=sekolah)
            siswa_instances = Siswa.objects.filter(sekolah=sekolah)

            for _ in range(20):
                Pelanggaran.objects.create(
                    sekolah=sekolah,
                    staff_sekolah=faker.random_element(staff_instances),
                    siswa=faker.random_element(siswa_instances),
                    pelanggaran_kategori=faker.random_element(pelanggaran_kategori_list),
                    pesan=faker.text()
                )

        self.stdout.write(self.style.SUCCESS('Successfully generated dummy data'))
