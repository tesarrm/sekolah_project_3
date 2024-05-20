from rest_framework import serializers
from .models import Sekolah, Tingkat, Jurusan, Kelas

# class SekolahSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Sekolah
#         fields = '__all__' 

class SekolahSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sekolah
        fields = ['id', 'nama', 'alamat', 'kota', 'provinsi', 'no_telp', 'email', 'website']


class TingkatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tingkat
        fields = '__all__' 

class JurusanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jurusan
        fields = '__all__' 

class KelasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kelas
        fields = ['id', 'nama', 'sekolah', 'tingkat']j