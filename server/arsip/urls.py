from django.urls import path, include
from .views import *


urlpatterns = [
    #root user
    path('super/', rootSuper),
    path('super/<str:department>/', rootDepartment, name='super-department'),
    path('super/<str:department>/<str:divisi>/', rootDivisi),
    path('super/users/', rootUser, name='super_user'),

    # general purpose
    path('demo-login/', demo_login),

    #list pilihan surat masuk dan keluar
    path('data/<str:de>/<str:di>/', demo_divisi, name='divisi'),
    # url surat masuk   
    path('data/<str:de>/<str:di>/suratmasuk/', demo_suratmasuk, name='suratmasuk'),
    path('data/<str:de>/<str:di>/suratmasuk/<str:filename>', demo_suratmasukdetail, name='suratmasukdetail'),
    # url surat keluar
    path('data/<str:de>/<str:di>/suratkeluar/', demo_suratkeluar, name='suratkeluar'),
    path('data/<str:de>/<str:di>/suratkeluar/<str:filename>', demo_suratkeluardetail, name='suratkeluardetail'),
    
    path('approve/', demo_approve),
    path('demo-upload/', demo_upload),
    path('logout/', logout, name='logout')
]

