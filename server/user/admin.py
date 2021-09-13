from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import *

admin.site.register(Pengguna)
admin.site.register(Department)
admin.site.register(TypeBerkas)
admin.site.register(JenisBerkas)
admin.site.register(Role)
admin.site.register(BerkasMasuk)
admin.site.register(BerkasKeluar)