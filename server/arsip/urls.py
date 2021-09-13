from django.urls import path, include
from .views import *


urlpatterns = [
    #root user
    path('super/', root),
    # general purpose
    path('demo-login/', demo_login),
    path('demo/<str:department>/', demo_department),
    path('demo/<str:department>/<str:detail>/', demo_detail),
    path('demo-upload/', demo_upload),
    path('logout/', logout, name='logout')
]

