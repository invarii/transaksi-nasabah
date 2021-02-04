from django.db import models

from api_sad_sig.util import CustomModel
from v1.models import SadPenduduk


class SuratDomisili(CustomModel):
    no_surat = models.CharField(max_length=50, blank=True, null=True)
    pegawai = models.ForeignKey(
        "v1.Pegawai", models.DO_NOTHING, blank=True, null=True
    )
    penduduk = models.ForeignKey(
        "v1.SadPenduduk", models.DO_NOTHING, blank=True, null=True
    )
    keperluan = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "surat_domisili"


class SuratSkck(CustomModel):
    no_surat = models.CharField(max_length=50, blank=True, null=True)
    pegawai = models.ForeignKey(
        "v1.Pegawai", models.DO_NOTHING, blank=True, null=True
    )
    penduduk = models.ForeignKey(
        "v1.SadPenduduk", models.DO_NOTHING, blank=True, null=True
    )
    keterangan = models.TextField(blank=True, null=True)
    keperluan = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "surat_skck"


class SuratKelahiran(CustomModel):
    no_surat = models.CharField(max_length=50, blank=True, null=True)
    pegawai = models.ForeignKey(
        "v1.Pegawai",
        models.DO_NOTHING,
        related_name="acc_surat_kelahiran",
        blank=True,
        null=True,
    )
    ayah = models.ForeignKey(
        "v1.SadPenduduk",
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="ayah_surat_lahir",
    )
    ibu = models.ForeignKey(
        "v1.SadPenduduk",
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="ibu_surat_lahir",
    )
    saksi1 = models.ForeignKey(
        "v1.Pegawai",
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="saksi1_surat_lahir",
    )
    saksi2 = models.ForeignKey(
        "v1.Pegawai",
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="saksi2_surat_lahir",
    )
    nama = models.CharField(max_length=100, blank=True, null=True)
    jk = models.CharField(max_length=15, blank=True, null=True)
    tempat_dilahirkan = models.ForeignKey(
        "v1.JenisTempat", models.DO_NOTHING, blank=True, null=True
    )
    tempat_kelahiran = models.CharField(max_length=50, blank=True, null=True)
    tgl = models.DateField(blank=True, null=True)
    jenis_kelahiran = models.ForeignKey(
        "v1.JenisKelahiran", models.DO_NOTHING, blank=True, null=True
    )
    kelahiran_ke = models.CharField(max_length=15, blank=True, null=True)
    penolong_kelahiran = models.ForeignKey(
        "v1.TenagaKesehatan", models.DO_NOTHING, blank=True, null=True
    )
    berat = models.CharField(max_length=15, blank=True, null=True)
    panjang = models.CharField(max_length=15, blank=True, null=True)

    @property
    def keterangan_tempat_dilahirkan(self):
        if self.tempat_dilahirkan:
            return self.tempat_dilahirkan.nama
        return None

    @property
    def keterangan_penolong_kelahiran(self):
        if self.penolong_kelahiran:
            return self.penolong_kelahiran.nama
        return None

    @property
    def keterangan_jenis_kelahiran(self):
        if self.jenis_kelahiran:
            return self.jenis_kelahiran.nama
        return None

    class Meta:
        db_table = "surat_kelahiran"


class SadKelahiran(CustomModel):
    nama = models.CharField(max_length=100, blank=True, null=True)
    jenis_kelamin = models.CharField(max_length=20, blank=True, null=True)
    tempat_dilahirkan = models.CharField(max_length=20, blank=True, null=True)
    tempat_kelahiran = models.CharField(max_length=20, blank=True, null=True)
    tanggal_kelahiran = models.DateField(blank=True, null=True)
    jam = models.TimeField(blank=True, null=True)
    jenis_kelahiran = models.CharField(max_length=20, blank=True, null=True)
    kelahiran_ke = models.CharField(max_length=5, blank=True, null=True)
    penolong_kelahiran = models.CharField(max_length=30, blank=True, null=True)
    berat_bayi = models.CharField(max_length=10, blank=True, null=True)
    panjang_bayi = models.CharField(max_length=10, blank=True, null=True)
    nik_ayah = models.CharField(max_length=16, blank=True, null=True)
    nik_ibu = models.CharField(max_length=16, blank=True, null=True)
    nama_ayah = models.CharField(max_length=100, blank=True, null=True)
    nama_ibu = models.CharField(max_length=100, blank=True, null=True)
    nama_pelapor = models.CharField(max_length=100, blank=True, null=True)
    nik_saksi_satu = models.CharField(max_length=16, blank=True, null=True)
    nik_saksi_dua = models.CharField(max_length=16, blank=True, null=True)

    def find_penduduk(self, element):
        reference = getattr(self, element)
        if reference:
            return SadPenduduk.objects.filter(nik=reference).first()
        return None

    @property
    def tanggal_kawin(self):
        ayah = self.find_penduduk("nik_ayah")
        if ayah:
            return ayah.tgl_kawin
        return None

    class Meta(CustomModel.Meta):

        db_table = "sad_kelahiran"


class SadKematian(CustomModel):
    penduduk = models.ForeignKey(
        "v1.SadPenduduk", models.DO_NOTHING, blank=True, null=True
    )
    tanggal_kematian = models.DateField(blank=True, null=True)
    jam = models.TimeField(blank=True, null=True)
    sebab_kematian = models.CharField(max_length=50, blank=True, null=True)
    tempat_kematian = models.CharField(max_length=50, blank=True, null=True)
    yang_menerangkan = models.CharField(max_length=50, blank=True, null=True)
    nama_pelapor = models.CharField(max_length=100, blank=True, null=True)
    nama_saksi_satu = models.CharField(max_length=100, blank=True, null=True)
    nama_saksi_dua = models.CharField(max_length=100, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sad_kematian"


class SadLahirmati(CustomModel):
    nama = models.CharField(max_length=100, blank=True, null=True)
    lama_kandungan = models.CharField(max_length=20, blank=True, null=True)
    jenis_kelamin = models.CharField(max_length=20, blank=True, null=True)
    tanggal_lahir = models.DateField(blank=True, null=True)
    jam = models.TimeField(blank=True, null=True)
    jenis_kelahiran = models.CharField(max_length=20, blank=True, null=True)
    kelahiran_ke = models.CharField(max_length=5, blank=True, null=True)
    tempat_dilahirkan = models.CharField(max_length=50, blank=True, null=True)
    penolong_kelahiran = models.CharField(max_length=50, blank=True, null=True)
    sebab_lahirmati = models.CharField(max_length=50, blank=True, null=True)
    yang_menentukan = models.CharField(max_length=50, blank=True, null=True)
    tempat_kelahiran = models.CharField(max_length=50, blank=True, null=True)
    nik_ayah = models.CharField(max_length=16, blank=True, null=True)
    nik_ibu = models.CharField(max_length=16, blank=True, null=True)
    nama_ayah = models.CharField(max_length=100, blank=True, null=True)
    nama_ibu = models.CharField(max_length=100, blank=True, null=True)
    nama_pelapor = models.CharField(max_length=100, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sad_lahirmati"


class JenisPindah(CustomModel):
    nama = models.CharField(max_length=64)
    label = models.CharField(max_length=128)

    def __str__(self):
        return self.label

    class Meta(CustomModel.Meta):
        db_table = "jenis_pindah"


class AlasanPindah(CustomModel):
    id = models.IntegerField(primary_key=True, default=1)
    nama = models.CharField(max_length=64, default="label")
    label = models.CharField(max_length=128, default="nama")

    def __str__(self):
        return self.label

    class Meta(CustomModel.Meta):
        db_table = "alasan_pindah"


class KlasifikasiPindah(CustomModel):
    id = models.IntegerField(primary_key=True, default=1)
    nama = models.CharField(max_length=64, default="label")
    label = models.CharField(max_length=128, default="nama")

    def __str__(self):
        return self.label

    class Meta(CustomModel.Meta):
        db_table = "klasifikasi_pindah"


class StatusKKTinggal(CustomModel):
    id = models.IntegerField(primary_key=True, default=1)
    nama = models.CharField(max_length=64, default="label")
    label = models.CharField(max_length=128, default="nama")

    def __str__(self):
        return self.label

    class Meta(CustomModel.Meta):
        db_table = "status_kk_tinggal"


class StatusKKPindah(CustomModel):
    id = models.IntegerField(primary_key=True, default=1)
    nama = models.CharField(max_length=64, default="label")
    label = models.CharField(max_length=128, default="nama")

    def __str__(self):
        return self.label

    class Meta(CustomModel.Meta):
        db_table = "status_kk_pindah"


class SadPindahKeluar(CustomModel):
    nomor_kk = models.CharField(max_length=54, default="")
    nik_pemohon = models.CharField(max_length=54, default="")
    alasan = models.ForeignKey(
        AlasanPindah,
        models.DO_NOTHING,
        related_name="data_keluar_alasan",
        blank=True,
        null=True,
    )
    kelurahan_tujuan = models.ForeignKey(
        "v1.SadDesa", models.DO_NOTHING, blank=True, null=True
    )
    dusun_tujuan = models.CharField(max_length=20, blank=True, null=True)
    rt_tujuan = models.CharField(max_length=5, blank=True, null=True)
    rw_tujuan = models.CharField(max_length=5, blank=True, null=True)
    kodepos_tujuan = models.CharField(max_length=5, blank=True, null=True)
    no_telp = models.CharField(max_length=13, blank=True, null=True)
    klasifikasi_pindah = models.ForeignKey(
        KlasifikasiPindah,
        models.DO_NOTHING,
        related_name="data_keluar_klasifikasi",
        blank=True,
        null=True,
    )
    jenis_kepindahan = models.ForeignKey(
        JenisPindah,
        models.DO_NOTHING,
        related_name="data_keluar_jenis",
        blank=True,
        null=True,
    )
    status_kk_pindah = models.ForeignKey(
        StatusKKPindah,
        models.DO_NOTHING,
        related_name="data_keluar_kk_pindah",
        blank=True,
        null=True,
    )
    status_kk_tinggal = models.ForeignKey(
        StatusKKTinggal,
        models.DO_NOTHING,
        related_name="data_keluar_kk_tinggal",
        blank=True,
        null=True,
    )
    rencana_tgl_pindah = models.DateField(blank=True, null=True)
    nik_pindah = models.CharField(max_length=72, default="")

    def anggota_keluar(self):
        nik_s = list(self.nik_pindah.split(","))
        if nik_s:
            return SadPenduduk.all_objects.filter(pk__in=nik_s)
        return []

    class Meta(CustomModel.Meta):

        db_table = "sad_pindah_keluar"


class SadPindahMasuk(CustomModel):
    no_kk = models.CharField(max_length=18, blank=True, null=True)
    status_kk_pindah = models.ForeignKey(
        StatusKKPindah, models.DO_NOTHING, blank=True, null=True
    )
    tanggal_kedatangan = models.DateField(blank=True, null=True)
    alamat = models.ForeignKey(
        "v1.Alamat", models.DO_NOTHING, blank=True, null=True
    )
    nik_datang = models.CharField(max_length=128, blank=True, null=True)

    def anggota_masuk(self):
        nik_s = list(self.nik_datang.split(","))
        if nik_s:
            return SadPenduduk.all_objects.filter(pk__in=nik_s)
        return []

    class Meta(CustomModel.Meta):

        db_table = "sad_pindah_masuk"


class SadPecahKK(CustomModel):
    keluarga = models.ForeignKey("v1.SadKeluarga", models.DO_NOTHING)
    penduduk = models.ManyToManyField("v1.SadPenduduk")
