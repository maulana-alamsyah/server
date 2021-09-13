from arsip.models import *


#View as department

# Get file for Staff at DEPARTMENT INFORMATIKA
d_informatika = Departemen.objects.get(departementName='Informatika')       #object
berkas = d_informatika.berkas_set.get(upload_for='ST')                      #QueryList

# Change read status
berkas = Berkas.objects.get(fileName='FOTO-2')
berkas.read_staff.all()                                         # Get all reader
berkas.read_staff.get(username='NAMA-USER')                     # Get specific reader
berkas.read_staff.readbyManager(username='NAMA-MANAGER')        # CHANGE specific reader


# List member of Department
d_keuangan = Departemen.objects.get(departementName='Keuangan')
list_member = d_keuangan.pengguna_set.all()                         # Get all member
member = d_keuangan.pengguna_set.get(username='NAMA-USER')          # Get specific user