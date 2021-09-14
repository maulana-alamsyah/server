from django.urls import path, include
from .views import *


urlpatterns = [
    #root user
    path('super/', rootSuper),
    path('super/<str:department>/', rootDepartment),
    path('super/<str:department>/<str:divisi>/', rootDivisi),
    # general purpose
    path('demo-login/', demo_login),
    path('demo-register/', demo_register),
    path('demo/<str:de>/<str:di>/', demo_divisi, name='divisi'),
    path('demo-upload/', demo_upload),
    path('logout/', logout, name='logout')
]

