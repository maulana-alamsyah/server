from django.db import models
import os
from django.db.models.fields.related import ManyToManyField
from django.utils import timezone

# Tabel Departemen/Divisi
class Departemen(models.Model):
    departementID = models.CharField(max_length=6, null=False)
    departementName = models.CharField(max_length=21, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    link_dir = models.CharField(null=True, max_length=40)

    def __str__(self):
        return self.departementName

# Tabel Role Karyawan (Staff, Manajer, dll)
class Role(models.Model):
    roleCode = models.CharField(max_length=4, null=False)
    roleName = models.CharField(max_length=16, null=False)

    def __str__(self):
        return self.roleName

# Tabel Jenis Berkas (Dinas, Selebaran, dll)
class JenisBerkas(models.Model):
    jenisCode = models.CharField(max_length=6)
    jenisName = models.CharField(max_length=16)

    def __str__(self):
        return self.jenisName

# Tabel Type Berkas (Biasa, Penting, Sangat Penting)
class TypeBerkas(models.Model):
    typeCode = models.CharField(max_length=3, null=False)
    typeName = models.CharField(max_length=16, null=False)

    def __str__(self):
        return self.typeName

# Tabel Pengguna
class Pengguna(models.Model):
    username = models.CharField(max_length=21, null=False)
    password = models.TextField(max_length=21, null=False)
    time_login = models.IntegerField(default=5000)
    state    = models.TextField(max_length=21, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)
    member_of = models.ManyToManyField(Departemen)

    def __str__(self):
        return (f'{self.username}')

# Tabel Berkas Masuk
class BerkasMasuk(models.Model):
    upload_to_departement = models.ManyToManyField(Departemen)
    upload_for = models.ManyToManyField(Role)
    file = models.FileField(upload_to='', null=True)
    fileName = models.CharField(max_length=120, default=file.name)
    jenisBerkas = models.ForeignKey(JenisBerkas, on_delete=models.CASCADE)
    typeBerkas = models.ForeignKey(TypeBerkas, on_delete=models.CASCADE)
    address_sender = models.CharField(max_length=160, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    sender = models.CharField(max_length=120, null=True)
    upload_by = models.ForeignKey(Pengguna, on_delete=models.CASCADE)
    read_staff = models.ManyToManyField(Pengguna, related_name='staff', blank=True)
    read_manager = models.ManyToManyField(Pengguna, related_name='manager', blank=True)
    approve = models.BooleanField(default=False)

    def __str__(self):
        return self.fileName

    def readbyStaff(self, objPegguna):
        self.read_staff.add(objPegguna)
        self.save()

    def readbyManager(self, objPengguna):
        self.read_manager.add(objPengguna)
        self.save()