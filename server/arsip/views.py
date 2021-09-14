from arsip.models import SuratKeluar
from .supervisor import Supervisor, QueryMaster
from django.shortcuts import redirect, render
from django.http.response import JsonResponse
import time,random, string
from django.views.decorators.clickjacking import xframe_options_exempt, xframe_options_sameorigin
from django.utils import timezone
from .models import *

supervisor = Supervisor()

def rand():
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(32))

def demo_login(request):
    if (request.method=='GET'):
        try:
            status, users = supervisor.authState(request.COOKIES['auth'])
        except:
            return render(request, 'demo_login.html')
        if (status==True):
            if (users.department.count() > 1):
                return redirect(f'/demo/{users.department.all()[0].url}/{users.divisi.all()[0].url}')
            else:
                return redirect(f'/demo/{users.department.all()[0].url}/{users.divisi.all()[0].url}')
        else:
            return render(request, 'demo_login.html')
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password1']
            status, users = supervisor.authLogin(username, password)
            print(f'\t[demo-login] {status} - POST and get cookie {users}')
        except:
            print(f'\t[demo-login] {status} - {users}')
            return redirect('/demo-login')
        if (status==True):
            if (users.department.count() > 1):
                ren = redirect(f'/demo/{users.department.all()[0].url}/{users.divisi.all()[0].url}')
                users.cookies = rand()
                users.save()
                print(f'\t[demo-login] New cookie : {users.cookies}')
                print(f'\t[demo-login] Set cookie : {users.cookies}')
                ren.set_cookie('auth', users.cookies, max_age=5000)
                return ren
            else:
                ren = redirect(f'/demo/{users.department.all()[0].url}/{users.divisi.all()[0].url}')
                users.cookies = rand()
                users.save()
                print(f'\t[demo-login] New cookie : {users.cookies}')
                print(f'\t[demo-login] Set cookie : {users.cookies}')
                ren.set_cookie('auth', users.cookies, max_age=5000)
                return ren
        else:
            print(f'\t[demo-login] {users.cookies}')
            return redirect('/demo-login')  

def demo_register(request):
    if(request.method=='GET'):
        return render(request, 'demo_register.html')
    else:
        return render(request, 'demo_register.html')

def demo_divisi(request, de, di):

    if (request.method=='GET'):
        try:
            #Get user cookie first
            status, users = supervisor.authState(request.COOKIES['auth'])
        except:
            return redirect('/demo-login')
        # got user data
        if (status==True):
            d_obj = users.department.all()[0]
            suratMasuk = SuratMasuk.objects.filter(department=d_obj)
            print(suratMasuk)
            return render(request, 'demo_divisi.html', context={'suratMasuk': suratMasuk})
        else:
            return redirect('/demo-login')
 
@xframe_options_exempt
def demo_detail(request, department, detail):
    if (request.method=='GET'):
        try:
            status, users = supervisor.authState(request.COOKIES['auth'])
        except:
            return redirect('/demo-login')
    if(status==True):
        departments = supervisor.getDepartment(department)
        berkasMasuk = departments.berkasmasuk_set.get(fileName=detail)
        berkasMasuk.read_staff.add(users)
        berkasMasuk.save()
        fl = f'/media/{berkasMasuk.file}'
        return render(request, 'demo_detail.html', context={
            'pdf_file': fl,
            'info_file': berkasMasuk,
            'users': users
        })

def demo_upload(request):
    spvsr = Supervisor()
    query = QueryMaster()
    status = None
    try:
        status, user = spvsr.authState(request.COOKIES['auth'])
    except:
        status = False
    if (status==True):
        if request.method == 'POST':
            level = request.POST['level']
            access = request.POST['access']
            upload_to = request.POST['upload-to']
            upload_for= request.POST['upload-for']
            upload_by = user
            fileID = 10
            files = request.FILE['file']
            filename = request.POST['filename']
            address_sender = request.POST['address']
            sender = request.POST['sender']
            try:
                status = query.create('BerkasMasuk')
                return redirect(request, '/demo-upload')
            except:
                return redirect(request, '/demo-upload')
        else:
            return render(request, 'demo_upload.html')
    else:
        return render(request, 'login.html')

def logout(request):
    resp = redirect('/demo-login')
    resp.delete_cookie('auth')
    return resp


##  _________________
##  |               |
##  | ROOT BACKEND  |
##  |               |
##  |_______________|

def rootSuper(request):
    if (request.method=='GET'):
        try:
            # GET COOKIE
            departments = supervisor.getAllDepartment()
            return render(request, 'root.html', context={
                'd_list': departments
            })
        except:
            print('EROR SAAT MENGAMBIL DATA')
    return render(request, 'root.html', context={})

def rootDepartment(request, department):
    if (request.method=='GET'):
        try:
            # GET COOKIE
            d_obj = supervisor.getDepartment(department)
            return render(request, 'root_department.html', context={
                'd_obj': d_obj
            })
        except:
            print('EROR SAAT MENGAMBIL DATA')
    return render(request, 'root.html', context={})

# tampilkan surat masuk dan keluar dalam divisi tsb
def rootDivisi(request, department, divisi):
    if (request.method=='GET'):
        try:
            # GET COOKIE
            sm_list = supervisor.getAllSuratMasuk(department, divisi)
            sk_list = supervisor.getAllSuratKeluar(department, divisi)
            return render(request, 'root_division.html', context={
                'sm_list': sm_list,
                'sk_list': sk_list
            })
        except:
            print('EROR SAAT MENGAMBIL DATA')
    return render(request, 'root.html', context={})