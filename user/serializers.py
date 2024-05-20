from rest_framework import serializers
from django.contrib.auth.models import User
from .models import SuperAdmin, AdminSekolah, StaffSekolah, Siswa, OrangTua
from akademik.models import Sekolah
from django.contrib.auth import authenticate
from akademik.serializers import KelasSerializer 

# CRUD

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class SuperAdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = SuperAdmin
        fields = '__all__'  

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        superadmin = SuperAdmin.objects.create(user=user, **validated_data)
        return superadmin

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            user_serializer = UserSerializer(instance=user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        instance.nama = validated_data.get('nama', instance.nama)
        instance.save()
        return instance

class AdminSekolahSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = AdminSekolah
        fields = '__all__'  

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        admin_sekolah = AdminSekolah.objects.create(user=user, **validated_data)
        return admin_sekolah

    # def create(self, validated_data):
    #     user_data = validated_data.pop('user')
    #     sekolah_data = validated_data.pop('sekolah')
        
    #     user = UserSerializer.create(UserSerializer(), validated_data=user_data)
    #     sekolah = Sekolah.objects.create(**sekolah_data)
        
    #     admin_sekolah = AdminSekolah.objects.create(user=user, sekolah=sekolah, **validated_data)
    #     return admin_sekolah

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            user_serializer = UserSerializer(instance=user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        instance.sekolah = validated_data.get('sekolah', instance.sekolah)
        instance.nama = validated_data.get('nama', instance.nama)
        instance.no_telp = validated_data.get('no_telp', instance.no_telp)
        instance.save()
        return instance

class StaffSekolahSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = StaffSekolah
        fields = '__all__'  

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        staff_sekolah = StaffSekolah.objects.create(user=user, **validated_data)
        return staff_sekolah

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            user_serializer = UserSerializer(instance=user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        instance.sekolah = validated_data.get('sekolah', instance.sekolah)
        instance.nama = validated_data.get('nama', instance.nama)
        instance.jabatan = validated_data.get('jabatan', instance.jabatan)
        instance.no_telp = validated_data.get('no_telp', instance.no_telp)
        instance.save()
        return instance

class SiswaSerializer(serializers.ModelSerializer):
    kelas = KelasSerializer()
    user = UserSerializer()

    class Meta:
        model = Siswa
        fields = '__all__'  

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        siswa = Siswa.objects.create(user=user, **validated_data)
        return siswa

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            user_serializer = UserSerializer(instance=user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        instance.sekolah = validated_data.get('sekolah', instance.sekolah)
        instance.nis = validated_data.get('nis', instance.nis)
        instance.nama = validated_data.get('nama', instance.nama)
        instance.kelas = validated_data.get('kelas', instance.kelas)
        instance.save()
        return instance

class OrangTuaSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = OrangTua
        fields = '__all__'  

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        orang_tua = OrangTua.objects.create(user=user, **validated_data)
        return orang_tua

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            user_serializer = UserSerializer(instance=user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        instance.siswa = validated_data.get('siswa', instance.siswa)
        instance.nama = validated_data.get('nama', instance.nama)
        instance.save()
        return instance

# Registration

class AdminSekolahRegistrationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class AdminSekolahRegistrationSekolahSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sekolah
        fields = '__all__'

class AdminSekolahRegistrationSerializer(serializers.ModelSerializer):
    user = AdminSekolahRegistrationUserSerializer()
    sekolah = AdminSekolahRegistrationSekolahSerializer()

    class Meta:
        model = AdminSekolah
        fields = '__all__' 

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        sekolah_data = validated_data.pop('sekolah')
        
        user = UserSerializer.create(AdminSekolahRegistrationUserSerializer(), validated_data=user_data)
        sekolah = Sekolah.objects.create(**sekolah_data)
        
        admin_sekolah = AdminSekolah.objects.create(user=user, sekolah=sekolah, **validated_data)
        return admin_sekolah

# Login

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

# class LoginSerializer(serializers.Serializer):
#     identifier = serializers.CharField()  # Bisa email atau username
#     password = serializers.CharField(write_only=True)

#     def validate(self, data):
#         identifier = data.get('identifier')
#         password = data.get('password')

#         if identifier and password:
#             # Cek apakah identifier adalah email atau username
#             if '@' in identifier:
#                 email = identifier
#                 try:
#                     user = User.objects.get(email=email)
#                 except User.DoesNotExist:
#                     # Buat pengguna baru jika tidak ada
#                     user = User.objects.create_user(username=email, email=email, password=password)
#             else:
#                 username = identifier
#                 try:
#                     user = User.objects.get(username=username)
#                 except User.DoesNotExist:
#                     raise serializers.ValidationError("Invalid login credentials.")
                
#             user = authenticate(request=self.context.get('request'), username=user.username, password=password)
#             if not user:
#                 raise serializers.ValidationError("Invalid login credentials.")
#         else:
#             raise serializers.ValidationError("Must include 'identifier' and 'password'.")

#         data['user'] = user
#         return data

# User detail current login

class UserDetailSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'  

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
        fields = '__all__'  

class AdminSekolahDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = AdminSekolah
        fields = '__all__'  

class StaffSekolahDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = StaffSekolah
        fields = '__all__'  

class SiswaDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = Siswa
        fields = '__all__'  

class OrangTuaDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = OrangTua
        fields = '__all__'  
