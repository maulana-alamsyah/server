from arsip.models import Pengguna
from django.contrib import admin
from .models import BerkasMasuk, Departemen, Pengguna, TypeBerkas, JenisBerkas, Role

# Register your models here.
admin.site.register(Pengguna)
admin.site.register(Departemen)
admin.site.register(BerkasMasuk)
admin.site.register(TypeBerkas)
admin.site.register(JenisBerkas)
admin.site.register(Role)