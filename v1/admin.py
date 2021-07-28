from django.contrib import admin

# Register your models here.

import v1.models as models

admin.site.register(models.Nasabah)
admin.site.register(models.Transaksi)
