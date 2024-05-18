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

# class SuperAdminSerializer(serializers.ModelSerializer):
#     user = UserSerializer()

#     class Meta:
#         model = SuperAdmin
#         fields = ['user', 'nama']

#     def create(self, validated_data):
#         user_data = validated_data.pop('user')
#         user = User.objects.create_user(**user_data)
#         superadmin = SuperAdmin.objects.create(user=user, **validated_data)
#         return superadmin

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

## Login

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


## User detail current login

class UserDetailSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type']

    def get_user_type(self, obj):
        if hasattr(obj, 'superadmin'):
            return 'SuperAdmin'
        elif hasattr(obj, 'adminsekolah'):
            return 'AdminSekolah'
        elif hasattr(obj, 'staffsekolah'):
            return 'StaffSekolah'
        elif hasattr(obj, 'siswa'):
            return 'Siswa'
        elif hasattr(obj, 'orangtua'):
            return 'OrangTua'
        return 'User'

class SuperAdminDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = SuperAdmin
        fields = ['user', 'nama']

class AdminSekolahDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = AdminSekolah
        fields = ['user', 'sekolah', 'nama', 'no_telp']

class StaffSekolahDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = StaffSekolah
        fields = ['user', 'sekolah', 'nama', 'jabatan', 'no_telp']

class SiswaDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = Siswa
        fields = ['user', 'sekolah', 'nis', 'nama', 'kelas']

class OrangTuaDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = OrangTua
        fields = ['user', 'siswa', 'nama']


## Register

class UserRegisterSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# class SuperAdminRegisterSerializer(serializers.ModelSerializer):
#     user = UserRegisterSerializer()

#     class Meta:
#         model = SuperAdmin
#         fields = ['user', 'nama']

#     def create(self, validated_data):
#         user_data = validated_data.pop('user')
#         user = User.objects.create_user(**user_data)
#         superadmin = SuperAdmin.objects.create(user=user, **validated_data)
#         return superadmin

class AdminSekolahRegisterSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer()

    class Meta:
        model = AdminSekolah
        fields = ['user', 'sekolah', 'nama', 'no_telp']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        admin_sekolah = AdminSekolah.objects.create(user=user, **validated_data)
        return admin_sekolah

# class StaffSekolahRegisterSerializer(serializers.ModelSerializer):
#     user = UserRegisterSerializer()

#     class Meta:
#         model = StaffSekolah
#         fields = ['user', 'sekolah', 'nama', 'jabatan', 'no_telp']

#     def create(self, validated_data):
#         user_data = validated_data.pop('user')
#         user = User.objects.create_user(**user_data)
#         staff_sekolah = StaffSekolah.objects.create(user=user, **validated_data)
#         return staff_sekolah

# class SiswaRegisterSerializer(serializers.ModelSerializer):
#     user = UserRegisterSerializer()

#     class Meta:
#         model = Siswa
#         fields = ['user', 'sekolah', 'nis', 'nama', 'kelas']

#     def create(self, validated_data):
#         user_data = validated_data.pop('user')
#         user = User.objects.create_user(**user_data)
#         siswa = Siswa.objects.create(user=user, **validated_data)
#         return siswa

# class OrangTuaRegisterSerializer(serializers.ModelSerializer):
#     user = UserRegisterSerializer()

#     class Meta:
#         model = OrangTua
#         fields = ['user', 'siswa', 'nama']

#     def create(self, validated_data):
#         user_data = validated_data.pop('user')
#         user = User.objects.create_user(**user_data)
#         orang_tua = OrangTua.objects.create(user=user, **validated_data)
#         return orang_tua
