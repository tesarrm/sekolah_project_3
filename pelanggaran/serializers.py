from rest_framework import serializers
from .models import Pelanggaran, PelanggaranKategori

class PelanggaranKategoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = PelanggaranKategori
        fields = '__all__'  

# class PelanggaranSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Pelanggaran
#         fields = '__all__'  

class PelanggaranSerializer(serializers.ModelSerializer):
    token_nobox = serializers.CharField(read_only=True)
    extId = serializers.CharField(read_only=True)
    accountId = serializers.CharField(read_only=True)
    body = serializers.CharField(read_only=True)

    class Meta:
        model = Pelanggaran
        fields = '__all__'
        extra_kwargs = {
            'token_nobox': {'read_only': True},
            'extId': {'read_only': True},
            'accountId': {'read_only': True},
            'body': {'read_only': True},
        }

    # def validate(self, data):
    #     if not data.get('token_nobox'):
    #         raise serializers.ValidationError({"token_nobox": "This field is required."})
    #     if not data.get('extId'):
    #         raise serializers.ValidationError({"extId": "This field is required."})
    #     if not data.get('accountId'):
    #         raise serializers.ValidationError({"accountId": "This field is required."})
    #     if not data.get('body'):
    #         raise serializers.ValidationError({"body": "This field is required."})
    #     return data
