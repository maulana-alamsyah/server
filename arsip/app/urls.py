from django.urls import path, include
from .views import *


urlpatterns = [
    #root user
    path('super/', rootSuper),
    path('super/homepage/', rootHomepage, name='super-homepage'),
    path('super/homepage/department/', rootDepartment),
    path('super/homepage/suratmasuk/', rootSuratmasuk),
    path('super/homepage/suratkeluar/', rootSuratkeluar),
    path('super/homepage/department/<str:divisi>', rootDivisi),
    path('super/users/', rootUser, name='super_user'),


    ## general purpose
    path('login/', login),
    path('homepage/', homepage, name='homepage'),
    # url surat masuk   
    path('homepage/suratmasuk/', suratmasuk, name='suratmasuk'),
    path('homepage/suratmasuk/<str:filename>', suratmasukdetail, name='suratmasukdetail'),
    # url surat keluar
    path('homepage/suratkeluar/', suratkeluar, name='suratkeluar'),
    path('homepage/suratkeluar/<str:filename>', suratkeluardetail, name='suratkeluardetail'),
    path('approve/<str:file>', approve),
    path('logout/', logout, name='logout')
]

