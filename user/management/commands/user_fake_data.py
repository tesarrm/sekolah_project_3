from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.models import User
from akademik.models import Sekolah, Kelas, Tingkat, Jurusan
from user.models import SuperAdmin, AdminSekolah, StaffSekolah, Siswa, OrangTua

faker = Faker()

class Command(BaseCommand):
    help = 'Generate dummy data for the application'

    def handle(self, *args, **kwargs):
        self.stdout.write("Generating dummy data...")

        # Clear existing data
        User.objects.all().delete()
        Sekolah.objects.all().delete()
        SuperAdmin.objects.all().delete()
        AdminSekolah.objects.all().delete()
        StaffSekolah.objects.all().delete()
        Siswa.objects.all().delete()
        OrangTua.objects.all().delete()

        # Create Sekolah instances
        for _ in range(5):
            sekolah = Sekolah.objects.create(
                nama=faker.company(),
                alamat=faker.address()
            )

            # Create SuperAdmin
            user = User.objects.create_user(username=faker.user_name(), password='password')
            SuperAdmin.objects.create(user=user, nama=faker.name())

            # Create AdminSekolah
            for _ in range(2):
                username = faker.user_name()
                while User.objects.filter(username=username).exists():
                    username = faker.user_name()
                user = User.objects.create_user(username=username, password='password')
                AdminSekolah.objects.create(user=user, sekolah=sekolah, nama=faker.name(), no_telp=faker.phone_number())

            # Create StaffSekolah
            for _ in range(5):
                username = faker.user_name()
                while User.objects.filter(username=username).exists():
                    username = faker.user_name()
                user = User.objects.create_user(username=username, password='password')
                StaffSekolah.objects.create(user=user, sekolah=sekolah, nama=faker.name(), jabatan=faker.job(), no_telp=faker.phone_number())

            # Create Kelas
            for tingkat in range(10, 13):
                for jurusan_name in ['IPA', 'MTK', 'IPS']:
                    tingkat_instance, _ = Tingkat.objects.get_or_create(nama=str(tingkat), sekolah=sekolah)
                    jurusan_instance, _ = Jurusan.objects.get_or_create(nama=jurusan_name, sekolah=sekolah)
                    nama_kelas = f"{tingkat}{jurusan_name}"
                    kelas = Kelas.objects.create(nama=nama_kelas, sekolah=sekolah, tingkat=tingkat_instance, jurusan=jurusan_instance)

                    # Create Siswa
                    for _ in range(5):
                        username = faker.user_name()
                        while User.objects.filter(username=username).exists():
                            username = faker.user_name()
                        user = User.objects.create_user(username=username, password='password')
                        siswa = Siswa.objects.create(user=user, sekolah=sekolah, nis=faker.unique.random_number(digits=5), nama=faker.name(), kelas=kelas)
                
                        # Create OrangTua for each Siswa
                        for _ in range(2):
                            username = faker.user_name()
                            while User.objects.filter(username=username).exists():
                                username = faker.user_name()
                            user = User.objects.create_user(username=username, password='password')
                            OrangTua.objects.create(user=user, siswa=siswa, nama=faker.name())

        self.stdout.write(self.style.SUCCESS('Successfully generated dummy data'))
