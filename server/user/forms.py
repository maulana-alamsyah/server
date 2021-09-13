from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, forms
from django.contrib.auth.models import User
from django.db.models.base import Model
from .models import Department, Pengguna, Role


class PenggunaRegister(UserCreationForm):
    class Meta:
        model = Pengguna
        fields = ['username', 'password1', 'password2', 'role', 'department']

    def user(self):
        obj = Pengguna.objects.get(username=self.cleaned_data['username'])
        return obj

    def saveDepartment(self):
        user = self.user()
        list_department = self.cleaned_data['department']
        for i in list_department:
            user.department.add(i)
            user.save()


class PenggunaLogin(UserCreationForm):
    class Meta:
        model = Pengguna
        fields = ['username', 'password1']
