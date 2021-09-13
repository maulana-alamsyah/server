import os
from django.utils import timezone, tree
import shutil
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

class Department(models.Model):
    departmentID = models.CharField(max_length=6, null=False)
    departmentName = models.CharField(max_length=21, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    link_dir = models.CharField(null=True, max_length=40)

    def __str__(self):
        return self.departmentName

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

class Pengguna(User):
    department = models.ManyToManyField(Department, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)

class File(models.Model):
    fileName = models.CharField(max_length=120, null=False)
    file = models.FileField(upload_to='', null=True)

    def __str__(self):
        return self.fileName

class BerkasMasuk(models.Model):

    # Tentang berkas
    linked_file = models.ManyToManyField(File, blank=True)
    sender = models.CharField(max_length=120, null=True)
    address_sender = models.CharField(max_length=160, null=False)
    jenisBerkas = models.ForeignKey(JenisBerkas, on_delete=models.CASCADE)
    typeBerkas = models.ForeignKey(TypeBerkas, on_delete=models.CASCADE)
    description = models.TextField(max_length=100)
    # Catatan Internal
    upload_to_departement = models.ManyToManyField(Department)
    upload_for = models.ManyToManyField(Role)
    created_at = models.DateTimeField(default=timezone.now)
    upload_by = models.ForeignKey(Pengguna, on_delete=models.CASCADE)
    approve_staff = models.ManyToManyField(Pengguna, related_name='staff', blank=True)
    approve_manager = models.ManyToManyField(Pengguna, related_name='manager', blank=True)
    all_approve = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)

    def __str__(self):
        return self.fileName

class BerkasKeluar(models.Model):

    # Tentang berkas
    linked_file = models.ManyToManyField(File, blank=True)
    destination = models.CharField(max_length=120, null=True)
    address_destination = models.CharField(max_length=160, null=False)
    jenisBerkas = models.ForeignKey(JenisBerkas, on_delete=models.CASCADE)
    typeBerkas = models.ForeignKey(TypeBerkas, on_delete=models.CASCADE)
    description = models.TextField(max_length=100)
    # Catatan Internal
    upload_from_departement = models.ManyToManyField(Department)
    created_at = models.DateTimeField(default=timezone.now)
    upload_by = models.ForeignKey(Pengguna, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)

    def __str__(self):
        return self.fileName
