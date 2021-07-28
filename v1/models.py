from datetime import date

from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404


class Nasabah(models.Model):
    name = models.CharField(max_length=200)

    class Meta:

        db_table = "nasabah"


class Transaksi(models.Model):
    transaction_date = models.DateTimeField(blank=True, auto_now_add=True, null=True)
    description = models.CharField(max_length=200)
    debit_credit_status = models.CharField(max_length=5)
    amount = models.IntegerField()

    class Meta:

        db_table = "transaksi"