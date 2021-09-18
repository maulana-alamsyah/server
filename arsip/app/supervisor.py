import os
from .models import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Supervisor():

    def __init__(self):
        pass

    # Create 'MEDIA' directory, return false if already exist
    def authenticate(self, request):
        ## Auth with cookie
        if (request.method=='GET'):
            try:
                reqCookie = request.COOKIES['auth']
                user = Pengguna.objects.get(cookies=reqCookie)
                return (True, user)
            except:
                return (False, None)

        ## auth with login
        if (request.method=='POST'):
            reqUsername = request.POST['namapengguna']
            reqPassword = request.POST['katasandi']
            try:
                user = Pengguna.objects.get(username=reqUsername)
                if (reqPassword==user.password):
                    return (True, user)
            except:
                return (False, None)

    def getDepartment(self, url):
        d_obj = Department.objects.get(url=url)
        return d_obj

    def getAllDepartment(self):
        d_obj = Department.objects.all()
        return d_obj

    def getAllSuratMasuk(self):
        s_list = SuratMasuk.objects.all()
        return s_list

    def getAllSuratKeluar(self):
        s_list = SuratKeluar.objects.all()
        return s_list

    def getSuratMasukfor(self, user):
        s_list = SuratMasuk.objects.filter(upload_for=user)
        return s_list

    def getSuratMasukNotifications(self, user):
        suratMasuk = SuratMasuk.objects.filter(upload_for=user)
        return suratMasuk.exclude(reader=user)

    def getFile(self, url):
        fl = File.objects.get(fileName=url)
        return fl

    def getSuratMasukByUrl(self, url):
        return SuratMasuk.objects.get(url=url)

    def checkApproving(self, sm_list, user):
        return sm_list.exclude(approve_by=user)
