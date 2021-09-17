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
    status, users = supervisor.authenticate(request)
    # status true success
    if (status):
        try:
            response = redirect(f'/data/{users.department.all()[0].url}/{users.divisi.all()[0].url}')
            users.cookies = rand()
            users.save()
            response.set_cookie('auth', users.cookies, max_age=5000)
            return response
        except:
            return JsonResponse({
                'status':500,
                'info': 'Error when try redirect!'})
    else:
        return render(request, 'demo_login.html')

def demo_divisi(request, de, di):
    status, user = supervisor.authenticate(request)
    if (status):
        user_department = user.get_department()
        sm_list = supervisor.getSuratMasukfor(user)
        sk_list = supervisor.getAllSuratKeluar(user_department)
        ## Notification
        notification_list = supervisor.getSuratMasukNotifications(user)
        return render(request, 'demo_divisi.html', context={
            'user': user,
            'notifications_list': notification_list,
            'sm_list': sm_list,
            'sk_list': sk_list})
    else:
        return redirect('/demo-login')
 
#list semua surat masuk
def demo_suratmasuk(request, de, di):
    status, user = supervisor.authenticate(request)
    if (status):
        user_department = user.get_department()
        sm_list = supervisor.getSuratMasukfor(user)
        ## Notification
        notification_list = supervisor.getSuratMasukNotifications(user)

        return render(request, 'demo_suratmasuk.html', context={
            'user': user,
            'department': user_department.url,
            'divisi': user.divisi.all()[0].url,
            'notifications_list': notification_list,
            'sm_list': sm_list,})
    else:
        return redirect('/demo-login')

@xframe_options_exempt
def demo_suratmasukdetail(request, de, di, filename):
    status, user = supervisor.authenticate(request)
    if (status):
        user_department = user.get_department()
        ## Notification
        file = supervisor.getFile(filename)
        suratmasuk = SuratMasuk.objects.get(url=filename)
        suratmasuk.reader.add(user)
        suratmasuk.save()
        notification_list = supervisor.getSuratMasukNotifications(user)
        suratmasuk = file.suratmasuk_set.all()[0]
        approve_by = suratmasuk.approve_by.all()
        suratmasuk = suratmasuk.reader.all()
        return render(request, 'demo_suratmasukdetail.html', context={
            'user' : user,
            'notifications_list': notification_list,
            'suratmasuk': suratmasuk,
            'file': file,
            'approve_list': approve_by
        })
    else:
        return redirect('/demo-login')

#list semua surat keluar
def demo_suratkeluar(request, de, di):
    status, user = supervisor.authenticate(request)
    if (status):
        user_department = user.get_department()
        sk_list = supervisor.getAllSuratKeluar(user_department)
        ## Notification
        notification_list = supervisor.getSuratMasukNotifications(user)

        return render(request, 'demo_suratkeluar.html', context={
            'user': user,
            'department': user_department.url,
            'divisi': user.divisi.all()[0].url,
            'notifications_list': notification_list,
            'sk_list': sk_list})
    else:
        return redirect('/demo-login')

def demo_suratkeluardetail(request, de, di, filename):
    status, user = supervisor.authenticate(request)
    if (status):
        user_department = user.get_department()
        sk_list = supervisor.getAllSuratKeluar(user_department)
        ## Notification
        notification_list = supervisor.getSuratMasukNotifications(user)

        return JsonResponse({'status':filename})
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

def logout(request):
    resp = redirect('/demo-login')
    resp.delete_cookie('auth')
    return resp

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

def demo_approve(request):
    fl = request.POST.get('namafile')
    user = Pengguna.objects.get(cookies=request.COOKIES['auth'])
    surat = SuratMasuk.objects.get(url=fl)
    surat.approve_by.add(user)
    return JsonResponse({
        'file': fl
    })




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
            print('EROR SAAT MENGAMBIL DATA SUPER')
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
            return redirect('super_user/')
    return render(request, 'root.html', context={})
# tampilkan surat masuk dan keluar dalam divisi tsb
def rootDivisi(request, department, divisi):
    if (request.method=='GET'):
        try:
            # GET COOKIE
            sm_list = SuratMasuk.objects.all()
            sk_list = SuratKeluar.objects.all()
            return render(request, 'root_division.html', context={
                'sm_list': sm_list,
                'sk_list': sk_list
            })
        except:
            print('EROR SAAT MENGAMBIL DATA DIVISI')
    return render(request, 'root.html', context={})

def rootUser(request):
    if (request.method=='GET'):
        try:
            # GET COOKIE
            users = Pengguna.objects.all()
            print(users)
            return render(request, 'root_users.html', context={
                'users': users
            })
        except:
            print('EROR SAAT MENGAMBIL DATA USER')
    return render(request, 'root.html', context={})
