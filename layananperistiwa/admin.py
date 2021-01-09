from django.contrib import admin

import layananperistiwa.models as models

admin.site.register(models.SadKelahiran)
admin.site.register(models.SadKematian)
admin.site.register(models.SadLahirmati)
admin.site.register(models.SadPindahKeluar)
admin.site.register(models.SadPindahMasuk)
admin.site.register(models.JenisPindah)
admin.site.register(models.KlasifikasiPindah)
admin.site.register(models.AlasanPindah)
admin.site.register(models.StatusKKTinggal)
admin.site.register(models.StatusKKPindah)
