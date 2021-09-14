import os
from .models import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Supervisor():

    d_list = Department.objects.all()

    def __init__(self):
        pass

    # Create 'MEDIA' directory, return false if already exist
    def createDir(self, nameDir):
        try:
            os.makedirs(f'../media/{nameDir}')
            return True
        except:
            return False

    def authState(self, reqState):
        try:
            user = Pengguna.objects.get(cookies=reqState)
            return (True, user)
        except:
            return (False, None)

    def authLogin(self, reqUsername, reqPassword):
        try:
            # Find Username
            user = Pengguna.objects.get(username=reqUsername)
            
            # if username exist and password match
            if reqPassword == user.password:
                print('Sukses login')
                return (True, user)
        except:
            return (False, None)


    def getDepartment(self, url):
        d_obj = Department.objects.get(url=url)
        return d_obj

    def getAllDepartment(self):
        d_obj = Department.objects.all()
        return d_obj

    def getAllSuratMasuk(self, department):
        s_list = SuratMasuk.objects.get(department=department)
        return s_list

    def getAllSuratKeluar(self, department):
        s_list = SuratKeluar.objects.filter(department=department)
        return s_list



class QueryMaster:

    d_list = Department.objects.all()
    p_list = Pengguna.objects.all()
    
    def listDepartement(self):
        return self.d_list

    def allFileAt(self, department, upload_for='EM'):
        try:
            d_list = Department.objects.get(departementName=department)
            print(department)
            depart = self.d_list.get(departementName=department)
            print(d_list)
            return (True, depart.berkas_set.all())
        except:
            return (False, None)

    def createBerkasMasuk(self, 
    level, access, upload_to, upload_for, upload_by, fileID, files, filename, address_sender, sender):
        try:
            obj = SuratMasuk(
                access = access,
                upload_to_department=upload_to,
                upload_for=upload_for,
                fileID=fileID,
                file=files,
                fileName=filename,
                level=level,
                address_sender=address_sender,
                sender=sender,
                upload_by=upload_by,
            )
            obj.save()
            return True
        except:
            return False