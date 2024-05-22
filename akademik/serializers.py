from rest_framework import serializers
from .models import Sekolah, Tingkat, Jurusan, Kelas
from pelanggaran.models import Pelanggaran

class SekolahSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sekolah
        fields = '__all__' 

class TingkatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tingkat
        fields = '__all__' 

class JurusanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jurusan
        fields = '__all__' 

class KelasSerializer(serializers.ModelSerializer):
    tingkat= TingkatSerializer()
    jurusan= JurusanSerializer()

    class Meta:
        model = Kelas
        fields = '__all__' 

    def get_jumlah_pelanggaran(self, obj):
        return Pelanggaran.objects.filter(siswa__kelas=obj).count()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['jumlah_pelanggaran'] = self.get_jumlah_pelanggaran(instance)
        return representation