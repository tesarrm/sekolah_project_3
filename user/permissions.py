from rest_framework import permissions

class IsSuperAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and hasattr(request.user, 'superadmin')

class IsAdminSekolahOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and hasattr(request.user, 'adminsekolah')

class IsSuperAdminAndAdminSekolahOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        is_superadmin = request.user.is_authenticated and hasattr(request.user, 'superadmin')
        is_admin_sekolah = request.user.is_authenticated and hasattr(request.user, 'adminsekolah')
        return is_superadmin or is_admin_sekolah

class IsStaffSekolahOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and hasattr(request.user, 'staffsekolah')

class IsSuperAdminAndAdminSekolahAndStaffSekolahOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        is_superadmin = request.user.is_authenticated and hasattr(request.user, 'superadmin')
        is_admin_sekolah = request.user.is_authenticated and hasattr(request.user, 'adminsekolah')
        is_staff_sekolah = request.user.is_authenticated and hasattr(request.user, 'staffsekolah')
        return is_superadmin or is_admin_sekolah or is_staff_sekolah

class IsSiswaOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and hasattr(request.user, 'siswa')

class IsOrangTuaOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and hasattr(request.user, 'orangtua')

#

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'superadmin')

class IsAdminSekolah(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'adminsekolah')

class IsStaffSekolah(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'staffsekolah')

class IsSiswa(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'siswa')

class IsOrangTua(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'orangtua')
