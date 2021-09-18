from django.shortcuts import redirect, render
from django.http.response import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from .supervisor import Supervisor
import random, string
from .models import Pengguna, SuratMasuk

supervisor = Supervisor()

def rand():
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(32))

def login(request):
    status, users = supervisor.authenticate(request)
    # status true success
    if (status):
        try:
            response = redirect(f'/homepage')
            users.cookies = rand()
            users.save()
            response.set_cookie('auth', users.cookies, max_age=5000)
            return response
        except:
            return JsonResponse({
                'status':500,
                'info': 'Error when try redirect!'})
    else:
        return render(request, 'login.html')

def logout(request):
    resp = redirect('/login')
    resp.delete_cookie('auth')
    return resp

def homepage(request):
    status, user = supervisor.authenticate(request)
    if (status):
        sm_list = supervisor.getSuratMasukfor(user)
        sk_list = supervisor.getAllSuratKeluar()
        ## Notification
        notification_list = supervisor.getSuratMasukNotifications(user)
        return render(request, 'homepage.html', context={
            'user': user,
            'notifications_list': notification_list,
            'sm_list': sm_list,
            'sk_list': sk_list})
    else:
        return redirect('/login')

def suratmasuk(request):
    status, user = supervisor.authenticate(request)
    if (status):
        sm_list = supervisor.getSuratMasukfor(user)
        unapprove = supervisor.checkApproving(sm_list, user)
        ## Notification
        notification_list = supervisor.getSuratMasukNotifications(user)

        return render(request, 'suratmasuk.html', context={
            'user': user,
            'notifications_list': notification_list,
            'sm_list': unapprove})
    else:
        return redirect('/login')

def suratkeluar(request):
    status, user = supervisor.authenticate(request)
    if(status):
        sk_list = supervisor.getAllSuratKeluar()
        notifications_list = supervisor.getSuratMasukNotifications(user)
    return render(request, 'suratkeluar.html', context={
        'user': user,
        'notifications_list': notifications_list,
        'sk_list': sk_list
    })

@xframe_options_exempt
def suratmasukdetail(request, filename):
    status, user = supervisor.authenticate(request)
    if (status):
        ## ambil file dan save reader
        file = supervisor.getFile(filename)
        suratmasuk = supervisor.getSuratMasukByUrl(filename)
        suratmasuk.reader.add(user)
        suratmasuk.save()
        # ambil approve dan reader
        approve_by = suratmasuk.approve_by.all()
        reader = suratmasuk.reader.all()

        return render(request, 'suratmasukdetail.html', context={
            'user' : user,
            'file': file,
            'reader_list': reader,
            'approve_list': approve_by
        })
    else:
        return redirect('/login')

def suratkeluardetail(request, filename):
    status, user = supervisor.authenticate(request)
    if (status):
        ## ambil file dan save reader
        file = supervisor.getFile(filename)
        return render(request, 'suratkeluardetail.html', context={
            'user' : user,
            'file': file,
        })
    else:
        return redirect('/login')

def approve(request, file):
    cookies = request.COOKIES['auth']
    try:
        user = Pengguna.objects.get(cookies=cookies)
        berkas = SuratMasuk.objects.get(url=file)
        berkas.approve_by.add(user)
        berkas.save()
        total_target = berkas.upload_for.all().count()
        total_approve = berkas.approve_by.all().count()
        if (total_target==total_approve):
            print('DATA COMPLETE SAVE KE ARSIP')
            return redirect('/homepage/suratmasuk')
        else:
            return redirect('/homepage/suratmasuk')
    except:
        print('WRONG LOGIC')


####
####    ROOT BACKEND
####

def rootSuper(request):

    if request.method == 'POST':
        if (request.POST['passcode']=='55555'):
            response = redirect('/super/homepage')
            return response
    else:
        resp = render(request, 'super.html')
        resp.delete_cookie('auth')
        return resp
        

def rootHomepage(request):
    if (request.method=='GET'):
        try:
            # GET COOKIE
            departments = supervisor.getAllDepartment()
            sm_list = supervisor.getAllSuratMasuk()
            sk_list = supervisor.getAllSuratKeluar()
            return render(request, 'super_homepage.html', context={
                'sm_list': sm_list,
                'sk_list': sk_list
            })
        except:
            print('EROR SAAT MENGAMBIL DATA SUPER')
    return render(request, 'super_homepage.html', context={})

def rootSuratmasuk(request):
    if (request.method=='GET'):
        try:
            return render(request, 'super_inputmasuk.html', context={})
        except:
            print('EROR SAAT MENGAMBIL DATA SUPER')
    return render(request, 'super_inputmasuk.html', context={})

def rootSuratkeluar(request):
    if (request.method=='GET'):
        try:
            return render(request, 'super_inputkeluar.html', context={})
        except:
            print('EROR SAAT MENGAMBIL DATA SUPER')
    return render(request, 'super_inputkeluar.html', context={})

def rootDepartment(request):
    pass

def rootDivisi(request):
    pass

def rootUser(request):
    pass
