from rest_framework import serializers
from .models import Pelanggaran, PelanggaranKategori
from akademik.models import Sekolah
from user.models import StaffSekolah, Siswa 
from user.serializers import UserDetailSerializer, StaffSekolahSerializer, SiswaSerializer
from akademik.serializers import SekolahSerializer


class PelanggaranKategoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = PelanggaranKategori
        fields = ['id', 'nama', 'poin', 'catatan']

class PelanggaranSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pelanggaran
        fields = '__all__'  

class PelanggaranNestedSerializer(serializers.ModelSerializer):
    sekolah = SekolahSerializer()
    staff_sekolah = StaffSekolahSerializer()
    siswa = SiswaSerializer()
    pelanggaran_kategori = PelanggaranKategoriSerializer()
    token_nobox = serializers.SerializerMethodField()
    extId = serializers.SerializerMethodField()
    accountId = serializers.SerializerMethodField()
    body = serializers.SerializerMethodField()

    class Meta:
        model = Pelanggaran
        fields = ['id', 'pesan', 'sekolah', 'staff_sekolah', 'siswa', 'pelanggaran_kategori', 'created_at', 'token_nobox', 'extId', 'accountId', 'body']

    def get_token_nobox(self, obj):
        return "token_nobox_value"

    def get_extId(self, obj):
        return "extId_value"

    def get_accountId(self, obj):
        return "accountId_value"

    def get_body(self, obj):
        return "body_value"
