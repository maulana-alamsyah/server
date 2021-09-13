import os
from .models import Departemen, Pengguna, BerkasMasuk

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Supervisor():

    d_list = Departemen.objects.all()

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
            user = Pengguna.objects.get(state=reqState)
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


    def getDepartment(self, link_dir):
        d_obj = Departemen.objects.get(link_dir=link_dir)
        return d_obj


class QueryMaster:

    d_list = Departemen.objects.all()
    p_list = Pengguna.objects.all()
    
    def listDepartement(self):
        return self.d_list

    def allFileAt(self, department, upload_for='EM'):
        try:
            d_list = Departemen.objects.get(departementName=department)
            print(department)
            depart = self.d_list.get(departementName=department)
            print(d_list)
            return (True, depart.berkas_set.all())
        except:
            return (False, None)

    def createBerkasMasuk(self, 
    level, access, upload_to, upload_for, upload_by, fileID, files, filename, address_sender, sender):
        try:
            obj = BerkasMasuk(
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