from os import stat
from django.db.models import query
from django.http.response import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from .models import Departemen, Pengguna
from .supervisor import Supervisor, QueryMaster
import time

# Create your views here.
def login(request):
    spvr = Supervisor()
    
    if request.method == 'POST':
        status, obj = spvr.authLogin(request.POST['username'], request.POST['password'])
        if status==True:
            ren = redirect('/demo-upload')
            ren.set_cookie('auth', 'abc')
            return ren
        else:
            return JsonResponse(data={'status': False})
        
    
    else:
        status = None    
        try:
            status, obj = spvr.authState(request.COOKIES['auth'])
        except:
            status = False
        if status:
            return redirect('/demo-upload')
        else:
            return render(request, 'login.html')


def home(request):
    return render(request, 'login.html')


def logout(request):
    resp = redirect('/demo-login')
    resp.delete_cookie('auth')
    return resp



def demo_login(request):
    ran = str(time.time())[::4]
    cursorDB = Supervisor()
    users = None
    Status = False
    if (request.method=='GET'):
        try:
            status, user = cursorDB.authState(request.COOKIES['auth'])
            users = user
        except:
            return render(request, 'demo_login.html')
        if (status==True):
            if (users.member_of.count() > 1):
                return redirect(f'/demo-{users.member_of.all()[0]}')
            else:
                return redirect(f'/demo-{users.member_of.all()[0]}')
        else:
            return render(request, 'demo_login.html')

    if request.method == 'POST':
        try:
            status, user = cursorDB.authLogin(request.POST['username'], request.POST['password'])
            users = user
        except:
            return redirect('/demo-login')
        if status==True:
            if (users.member_of.count() > 1):
                ren = redirect(f'/demo-{users.member_of.all()[0]}')
                users.state = ran
                users.save()
                ren.set_cookie('auth', ran, max_age=5000)
                return ren
            else:
                ren = redirect(f'/demo-{users.member_of.all()[0]}')
                users.state = ran
                users.save()
                ren.set_cookie('auth', ran, max_age=5000)
                return ren
        else:
            return redirect('/demo-login')



def demo_department(request, department):
    cursorDB = Supervisor()
    users = None
    if (request.method=='GET'):
        try:
            status, user = cursorDB.authState(request.COOKIES['auth'])
            users = user
            print(f'\t[demo_department] - status={status} ')
        except:
            return redirect('/demo-login')
        
        # got user data
        if (status==True):
            usersAccess = users.privileges
            d_obj = cursorDB.getDepartment(department)
            validator = False
            
            # Registered Department verif
            if users.member_of.count() > 1:
                for i in users.member_of.all():
                    if (i.departementName==department):
                        berkas = d_obj.berkasmasuk_set.filter(upload_for=usersAccess)
                        validator = True
                if validator==False:
                    return JsonResponse({'status': 'Access Denied!'})
            else:
                if users.member_of.all()[0].departementName == department:
                    berkas = d_obj.berkasmasuk_set.filter(upload_for=usersAccess)
                else:
                    return JsonResponse({'status': 'Access Denied!'})
            return render(request, 'demo_department.html', context={'file':berkas, 'd_obj': d_obj})
        else:
            return redirect('/demo-login')


def demo_detail(request, source):
    query = QueryMaster()





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