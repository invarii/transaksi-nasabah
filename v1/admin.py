from django.contrib import admin

# Register your models here.

import v1.models as models

admin.site.register(models.Pegawai)
admin.site.register(models.SadProvinsi)
admin.site.register(models.SadKabKota)
admin.site.register(models.SadKecamatan)
admin.site.register(models.SadDesa)
admin.site.register(models.BatasDesa)
admin.site.register(models.SadDusun)
admin.site.register(models.SadRt)
admin.site.register(models.SadRw)
admin.site.register(models.SadKeluarga)
admin.site.register(models.SadPenduduk)
admin.site.register(models.SadSarpras)
admin.site.register(models.SadInventaris)
admin.site.register(models.SadSurat)
admin.site.register(models.SadDetailSurat)
admin.site.register(models.SigPemilik)
admin.site.register(models.SigBidang)
admin.site.register(models.SigDesa)
admin.site.register(models.SigDukuh)
admin.site.register(models.SigDusun)
admin.site.register(models.SigRw)
admin.site.register(models.SigRt)
admin.site.register(models.Slider)
admin.site.register(models.KategoriArtikel)
admin.site.register(models.Artikel)
admin.site.register(models.KategoriInformasi)
admin.site.register(models.Informasi)
admin.site.register(models.KategoriPotensi)
# admin.site.register(models.Potensi)
admin.site.register(models.KategoriLapor)
admin.site.register(models.Lapor)
