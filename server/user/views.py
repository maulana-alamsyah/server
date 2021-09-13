from django.http import request
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import logout, login, authenticate
from arsip.supervisor import Supervisor
from .forms import PenggunaRegister, PenggunaLogin
from .models import *
from django.contrib import messages

# Create your views here.

def register(req):
    if req.method=='POST':
        form = PenggunaRegister(req.POST)
        print(req.POST.getlist('department'))
        if form.is_valid():
            form.save()
            form.saveDepartment()
            return redirect('demo-login')
        else:
            print(messages.error(req, 'Error'))

    else:
        form = PenggunaRegister()
        context ={
         'form': form,
        }   
        return render(req, 'demo_register.html', context=context)


def login(req):
    if req.method=='POST':
        form = PenggunaLogin(req.POST)
        username = req.POST.get('username')
        password = req.POST.get('password1')
        print(f'\nLogin with [{username}]:[{password}]')
        if form.is_valid():
            #auth here
            user = authenticate(username=username, password=password)
            print(user)
            return JsonResponse(data={'status':'200OK'})
        else:
            print(messages.error(req, 'Error'))
            return redirect('demo-login')
    else:
        form = PenggunaLogin()
    
        context ={
            'form': form,
        }
        return render(req, 'demo_login.html', context=context)


def logout(req):
    logout(req)
    return redirect('demo-login')