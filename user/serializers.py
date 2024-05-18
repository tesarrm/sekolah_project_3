from rest_framework import serializers
from django.contrib.auth.models import User
from .models import SuperAdmin, AdminSekolah, StaffSekolah, Siswa, OrangTua
from akademik.models import Sekolah

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class SuperAdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = SuperAdmin
        fields = ['user', 'nama']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        superadmin = SuperAdmin.objects.create(user=user, **validated_data)
        return superadmin

class AdminSekolahSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = AdminSekolah
        fields = ['user', 'sekolah', 'nama', 'no_telp']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        admin_sekolah = AdminSekolah.objects.create(user=user, **validated_data)
        return admin_sekolah

class StaffSekolahSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = StaffSekolah
        fields = ['user', 'sekolah', 'nama', 'jabatan', 'no_telp']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        staff_sekolah = StaffSekolah.objects.create(user=user, **validated_data)
        return staff_sekolah

class SiswaSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Siswa
        fields = ['user', 'sekolah', 'nis', 'nama', 'kelas']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        siswa = Siswa.objects.create(user=user, **validated_data)
        return siswa

class OrangTuaSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = OrangTua
        fields = ['user', 'siswa', 'nama']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        orang_tua = OrangTua.objects.create(user=user, **validated_data)
        return orang_tua


# Authentication 

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            from django.contrib.auth import authenticate
            user = authenticate(request=self.context.get('request'), username=username, password=password)

            if not user:
                raise serializers.ValidationError('Invalid credentials', code='authorization')

        else:
            raise serializers.ValidationError('Must include "username" and "password".')

        data['user'] = user
        return data