from django.db import models
import os
from django.db.models.fields.related import ManyToManyField
from django.utils import timezone

# Tabel Departemen
class Department(models.Model):
    departementID = models.CharField(max_length=6, null=False)
    departementName = models.CharField(max_length=21, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    url = models.CharField(null=True, max_length=40)
    status = models.BooleanField(default=True)    
    
    def __str__(self):
        return self.departementName

# Tabel Divisi
class Divisi(models.Model):
    divisiID = models.CharField(max_length=6, null=False)
    divisiName = models.CharField(max_length=21, null=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    url = models.CharField(null=True, max_length=40)
    status = models.BooleanField(default=True)
    
    def __str__(self):
        department = str(self.department)
        return (f'{self.divisiName} - {department}')

# Tabel Role Karyawan (Staff, Manajer, dll)
class Role(models.Model):
    roleCode = models.CharField(max_length=4, null=False)
    roleName = models.CharField(max_length=16, null=False)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.roleName

# Tabel Jenis Berkas (Dinas, Selebaran, dll)
class JenisBerkas(models.Model):
    jenisCode = models.CharField(max_length=6)
    jenisName = models.CharField(max_length=16)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.jenisName

# Tabel Pengguna
class Pengguna(models.Model):
    username = models.CharField(max_length=21, null=False)
    password = models.TextField(max_length=21, null=False)
    nik = models.TextField(max_length=60, blank=True)
    qr_code = models.IntegerField(null=False)
    time_login = models.IntegerField(default=5000)
    cookies    = models.TextField(max_length=21, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)
    department = models.ManyToManyField(Department)
    divisi = models.ManyToManyField(Divisi)
    status = models.BooleanField(default=True)

    def __str__(self):
        return (f'{self.username}')

# Table file
class File(models.Model):
    fileName = models.CharField(max_length=120)
    file = models.FileField(upload_to='', null=False)
    status = models.BooleanField(default=True)

# Tabel Berkas Masuk
class SuratMasuk(models.Model):
    TYPE_BERKAS = [('B', 'Biasa'), ('P', 'Penting'), ('SP', 'Sangat Penting')]
    file = models.ManyToManyField(File)
    fileName = models.CharField(max_length=120, default=file.name)
    jenisBerkas = models.ForeignKey(JenisBerkas, on_delete=models.CASCADE)
    typeBerkas = models.CharField(choices=TYPE_BERKAS, max_length=10,default='B')
    # general purpose
    department = models.ManyToManyField(Department)
    upload_for = models.ManyToManyField(Pengguna, related_name='target')
    address_sender = models.CharField(max_length=160, null=True)
    sender = models.CharField(max_length=120, null=True)
    description = models.CharField(max_length=60)
    upload_by = models.ForeignKey(Pengguna, related_name='uploaded', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    ## Berkas workflow
    reader = models.ManyToManyField(Pengguna, related_name='reader', blank=True)
    signature = models.ManyToManyField(Pengguna, related_name='signature', blank=True)
    approve_by = models.ManyToManyField(Pengguna, related_name='approved', blank=True)
    # status active/inactive file
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.fileName

    def readbyStaff(self, objPegguna):
        self.read_staff.add(objPegguna)
        self.save()

    def readbyManager(self, objPengguna):
        self.read_manager.add(objPengguna)
        self.save()

# Tabel Berkas Masuk
class SuratKeluar(models.Model):
    TYPE_BERKAS = [('B', 'Biasa'), ('P', 'Penting'), ('SP', 'Sangat Penting')]
    file = models.ManyToManyField(File)
    fileName = models.CharField(max_length=120, default=file.name)
    jenisBerkas = models.ForeignKey(JenisBerkas, on_delete=models.CASCADE)
    typeBerkas = models.CharField(choices=TYPE_BERKAS, max_length=16,default='B')
    # general purpose
    department = models.ManyToManyField(Department)
    destination_address = models.CharField(max_length=160, null=True)
    description = models.CharField(max_length=60)
    upload = models.ForeignKey(Pengguna, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    # status active/inactive file
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.fileName




##
##      DELETED TABLE
##
## Tabel Type Berkas (Biasa, Penting, Sangat Penting)
##  class TypeBerkas(models.Model):
##      typeCode = models.CharField(max_length=3, null=False)
##      typeName = models.CharField(max_length=16, null=False)
##  
##      def __str__(self):
##          return self.typeName
