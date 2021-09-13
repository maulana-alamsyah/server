from django.urls import path, include
from .views import register, login, logout

urlpatterns = [
    path('demo-register/', register, name='demo-register'),
    path('demo-login/', login, name='demo-login'),
    path('demo-logout/', logout, name='logout'),
]

