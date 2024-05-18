from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from user.models import Siswa, AdminSekolah, StaffSekolah, SuperAdmin

class NISBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            siswa = Siswa.objects.get(nis=username)
            if siswa.user.check_password(password):
                return siswa.user
        except Siswa.DoesNotExist:
            return None
        return None

class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
