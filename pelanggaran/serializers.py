from rest_framework import serializers
from .models import Pelanggaran, PelanggaranKategori

class PelanggaranKategoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = PelanggaranKategori
        fields = '__all__'  

class PelanggaranSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pelanggaran
        fields = '__all__'  
