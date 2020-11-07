from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Pegawai)
admin.site.register(SadProvinsi)
admin.site.register(SadKabKota)
admin.site.register(SadKecamatan)
admin.site.register(SadDesa)
admin.site.register(SadDusunDukuh)
admin.site.register(SadRt)
admin.site.register(SadRw)
admin.site.register(SadKeluarga)
admin.site.register(SadPenduduk)
admin.site.register(SadKelahiran)
admin.site.register(SadKematian)
admin.site.register(SadLahirmati)
admin.site.register(SadPindahKeluar)
admin.site.register(SadPindahMasuk)
admin.site.register(SadSarpras)
admin.site.register(SadInventaris)
admin.site.register(SadSurat)
admin.site.register(SadDetailSurat)