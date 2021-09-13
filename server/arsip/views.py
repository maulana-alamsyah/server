from .supervisor import Supervisor, QueryMaster
from django.shortcuts import redirect, render
from django.http.response import JsonResponse
import time,random, string
from django.views.decorators.clickjacking import xframe_options_exempt, xframe_options_sameorigin
from django.utils import timezone

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
            if (users.member_of.count() > 1):
                return redirect(f'/demo/{users.member_of.all()[0].link_dir}')
            else:
                return redirect(f'/demo/{users.member_of.all()[0].link_dir}')
        else:
            return render(request, 'demo_login.html')
    if request.method == 'POST':
        print('POST')
        try:
            username = request.POST['username']
            password = request.POST['password1']
            print(f'{username}--{password}')
            status, users = supervisor.authLogin(username, password)
            print(f'\t[demo-login] {status} - POST and get cookie {users}')
        except:
            print(f'\t[demo-login] {status} - {users}')
            return redirect('/demo-login')
        if (status==True):
            if (users.member_of.count() > 1):
                ren = redirect(f'/demo/{users.member_of.all()[0].link_dir}')
                users.state = rand()
                users.save()
                print(f'\t[demo-login] New cookie : {users.state}')
                print(f'\t[demo-login] Set cookie : {users.state}')
                ren.set_cookie('auth', users.state, max_age=5000)
                return ren
            else:
                ren = redirect(f'/demo/{users.member_of.all()[0].link_dir}')
                users.state = rand()
                users.save()
                print(f'\t[demo-login] New cookie : {users.state}')
                print(f'\t[demo-login] Set cookie : {users.state}')
                ren.set_cookie('auth', users.state, max_age=5000)
                return ren
        else:
            print(f'\t[demo-login] {users.state}')
            return redirect('/demo-login')  

def demo_department(request, department):
    if (request.method=='GET'):
        try:
            print("\t[demo-department] Get cookies : ", request.COOKIES['auth'])
            status, users = supervisor.authState(request.COOKIES['auth'])
            print(f'\t[demo-department] - {status} ')
        except:
            return redirect('/demo-login')
        # got user data
        if (status==True):
            role = users.role
            departments = supervisor.getDepartment(department)
            # Registered Department verif
            if users.member_of.count() > 1:
                for i in users.member_of.all():
                    if (i.link_dir==department):
                        berkasMasuk = departments.berkasmasuk_set.filter(upload_for=role)
                        validator = True
                if validator==False:
                    return JsonResponse({'status': 'Access Denied!'})
            else:
                if users.member_of.all()[0].link_dir == department:
                    berkasMasuk = departments.berkasmasuk_set.filter(upload_for=role)
                else:
                    print("HERE")
                    return JsonResponse({'status': 'Access Denied!'})
            return render(request, 'demo_department.html', context={
                'file':berkasMasuk,
                'd_obj': departments })
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

def root(request):
    return render(request, 'root.html', context={})