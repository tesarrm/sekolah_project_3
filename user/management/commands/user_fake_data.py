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

        # Create SuperAdmin
        user = User.objects.create_user(username=faker.user_name(), password='password')
        SuperAdmin.objects.create(user=user, nama=faker.name())

        # Create Sekolah
        for _ in range(3):
            sekolah = Sekolah.objects.create(
                nama=faker.company(),
                alamat=faker.address(),
                kota=faker.city(),
                provinsi=faker.state(),
                no_telp=faker.phone_number(),
                email=faker.email(),
                website=faker.url(),
                catatan=faker.text()
            )

            # Create AdminSekolah
            # for _ in range(2):
            username = faker.user_name()
            while User.objects.filter(username=username).exists():
                username = faker.user_name()
            user = User.objects.create_user(username=username, password='password')
            AdminSekolah.objects.create(
                user=user, 
                sekolah=sekolah, 
                nama=faker.name(), 
                no_telp=faker.phone_number()
            )

            # Create StaffSekolah
            for _ in range(3):
                username = faker.user_name()
                while User.objects.filter(username=username).exists():
                    username = faker.user_name()
                user = User.objects.create_user(username=username, password='password')
                StaffSekolah.objects.create(
                    user=user, 
                    sekolah=sekolah, 
                    nama=faker.name(), 
                    jabatan=faker.job(), 
                    no_telp=faker.phone_number()
                )

            # Create Kelas
            for tingkat_name in range(10, 13):
                for jurusan_name in ['IPA', 'MTK', 'IPS']:
                    tingkat = Tingkat.objects.create(nama=str(tingkat_name), sekolah=sekolah)
                    jurusan = Jurusan.objects.create(nama=jurusan_name, sekolah=sekolah)
                    for kelas_name in ['A', 'B', 'C']:
                        kelas = Kelas.objects.create(
                            nama=kelas_name, 
                            sekolah=sekolah, 
                            tingkat=tingkat, 
                            jurusan=jurusan
                        )

                        # Membuat OrangTua
                        orangtua_list = []
                        for _ in range(4):
                            username = faker.user_name()
                            while User.objects.filter(username=username).exists():
                                username = faker.user_name()
                            user = User.objects.create_user(username=username, password='password')
                            orangtua = OrangTua.objects.create(
                                user=user, 
                                nama=faker.name(),
                                no_telp=faker.phone_number()
                             )
                            orangtua_list.append(orangtua)

                        # Membuat Siswa dan assign ke OrangTua secara acak
                        for _ in range(5):
                            username = faker.user_name()
                            while User.objects.filter(username=username).exists():
                                username = faker.user_name()
                            user = User.objects.create_user(username=username, password='password')
                            orangtua = faker.random_element(elements=orangtua_list)
                            siswa = Siswa.objects.create(
                                user=user, 
                                sekolah=sekolah, 
                                kelas=kelas, 
                                nis=faker.unique.random_number(digits=5), 
                                nama=faker.name(), 
                                orangtua=orangtua, 
                                catatan=faker.text()
                            )    

        self.stdout.write(self.style.SUCCESS('Successfully generated dummy data'))
