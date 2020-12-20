import os
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField


def file_destination(instance, filename):
    extension = os.path.splitext(filename)[1]
    new_filename = timezone.now().strftime("%Y%m%d%H%M%S")
    folder_name = instance.__class__.__name__.lower()
    return f"{folder_name}/{new_filename}{extension}"


class CustomModelQuerySet(models.QuerySet):
    def delete(self):
        return super().update(deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class CustomModelManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop("alive_only", True)
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return CustomModelQuerySet(self.model).filter(deleted_at=None)
        return CustomModelQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class CustomModel(models.Model):
    created_at = models.DateTimeField(blank=True, auto_now_add=True, null=True)
    updated_at = models.DateTimeField(blank=True, auto_now=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="created_%(class)ss",
        blank=True,
        null=True,
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="updated_%(class)ss",
    )
    deleted_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="deleted_%(class)ss",
    )

    # Untuk query object hidup gunakan model_name.objects
    # Untuk query semua object gunakan model.all_objects
    objects = CustomModelManager()
    all_objects = CustomModelManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        # Tidak menghapus record dari database
        # hanya menandai bahwa data ini sudah tidak aktif
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        # Menghapus data dari database
        super().delete()


class Pegawai(CustomModel):
    nip = models.CharField(max_length=18, blank=True, null=True)
    nama = models.CharField(max_length=50, blank=True, null=True)
    jabatan = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(max_length=30, blank=True, null=True)
    golongan = models.CharField(max_length=30, blank=True, null=True)
    gambar = models.ImageField(
        upload_to=file_destination, blank=True, null=True
    )

    class Meta(CustomModel.Meta):

        db_table = "pegawai"


class SadProvinsi(CustomModel):
    kode_provinsi = models.CharField(max_length=5, blank=True, null=True)
    nama_provinsi = models.CharField(max_length=50, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sad_provinsi"


class SadKabKota(CustomModel):
    provinsi = models.ForeignKey(
        "SadProvinsi", models.DO_NOTHING, blank=True, null=True
    )
    kode_kab_kota = models.CharField(max_length=5, blank=True, null=True)
    nama_kab_kota = models.CharField(max_length=50, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sad_kab_kota"


class SadKecamatan(CustomModel):
    kab_kota = models.ForeignKey(
        SadKabKota, models.DO_NOTHING, blank=True, null=True
    )
    kode_kecamatan = models.CharField(max_length=5, blank=True, null=True)
    nama_kecamatan = models.CharField(max_length=250, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sad_kecamatan"


class SadDesa(CustomModel):
    id = models.BigAutoField(primary_key=True)
    kecamatan = models.ForeignKey(
        "SadKecamatan", models.DO_NOTHING, blank=True, null=True
    )
    kode_desa = models.CharField(max_length=5, blank=True, null=True)
    nama_desa = models.CharField(max_length=250, blank=True, null=True)
    alamat = models.CharField(max_length=150, blank=True, null=True)
    no_telp = models.CharField(max_length=12, blank=True, null=True)
    kode_pos = models.CharField(max_length=5, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    visi_misi = models.TextField(blank=True, null=True)
    sejarah = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to=file_destination, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sad_desa"


class BatasDesa(CustomModel):
    desa = models.ForeignKey(
        "SadDesa", models.DO_NOTHING, blank=True, null=True
    )
    utara = models.CharField(max_length=50, blank=True, null=True)
    selatan = models.CharField(max_length=50, blank=True, null=True)
    timur = models.CharField(max_length=50, blank=True, null=True)
    barat = models.CharField(max_length=50, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "batas_desa"


class SadDusun(CustomModel):
    desa = models.ForeignKey(
        "SadDesa", models.DO_NOTHING, blank=True, null=True
    )
    nama = models.CharField(max_length=70, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sad_dusun"


class SadRt(CustomModel):
    rw = models.ForeignKey("SadRw", models.DO_NOTHING, blank=True, null=True)
    rt = models.CharField(max_length=10, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sad_rt"


class SadRw(CustomModel):
    dusun = models.ForeignKey(
        SadDusun, models.DO_NOTHING, blank=True, null=True
    )
    rw = models.CharField(max_length=10, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sad_rw"


class SadKeluarga(CustomModel):
    no_kk = models.CharField(max_length=16, unique=True)
    alamat = models.CharField(max_length=100, blank=True, null=True)
    rt = models.ForeignKey("SadRt", models.DO_NOTHING, blank=True, null=True)
    kode_pos = models.CharField(max_length=5, blank=True, null=True)
    status_kesejahteraan = models.CharField(
        max_length=30, blank=True, null=True
    )
    penghasil = models.IntegerField(blank=True, null=True)
    status_kk = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.no_kk

    class Meta(CustomModel.Meta):

        db_table = "sad_keluarga"


class SadPenduduk(CustomModel):
    keluarga = models.ForeignKey(
        SadKeluarga,
        to_field="no_kk",
        on_delete=models.DO_NOTHING,
        related_name="anggota",
        blank=True,
        null=True,
    )
    user = models.OneToOneField(
        User,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="profile",
    )

    nik = models.CharField(max_length=16, unique=True)
    chip_ektp = models.CharField(max_length=10, blank=True, null=True)
    nama = models.CharField(max_length=50, blank=True, null=True)
    tgl_lahir = models.DateField(blank=True, null=True)
    tempat_lahir = models.CharField(max_length=50, blank=True, null=True)
    jk = models.CharField(max_length=12, blank=True, null=True)
    alamat = models.CharField(max_length=100, blank=True, null=True)
    agama = models.CharField(max_length=20, blank=True, null=True)
    pendidikan = models.CharField(max_length=20, blank=True, null=True)
    pekerjaan = models.CharField(max_length=50, blank=True, null=True)
    status_kawin = models.CharField(max_length=20, blank=True, null=True)
    status_penduduk = models.CharField(max_length=20, blank=True, null=True)
    kewarganegaraan = models.CharField(max_length=5, blank=True, null=True)
    anak_ke = models.CharField(max_length=5, blank=True, null=True)
    golongan_darah = models.CharField(max_length=5, blank=True, null=True)
    status_dalam_keluarga = models.CharField(
        max_length=20, blank=True, null=True
    )
    no_paspor = models.CharField(max_length=20, blank=True, null=True)
    suku = models.CharField(max_length=20, blank=True, null=True)
    potensi_diri = models.CharField(max_length=50, blank=True, null=True)
    no_hp = models.CharField(max_length=13, blank=True, null=True)
    nik_ayah = models.CharField(max_length=18, blank=True, null=True)
    nik_ibu = models.CharField(max_length=18, blank=True, null=True)
    nama_ayah = models.CharField(max_length=45, blank=True, null=True)
    nama_ibu = models.CharField(max_length=45, blank=True, null=True)
    tgl_exp_paspor = models.DateField(blank=True, null=True)
    akta_lahir = models.CharField(max_length=18, blank=True, null=True)
    akta_kawin = models.CharField(max_length=18, blank=True, null=True)
    tgl_kawin = models.DateField(blank=True, null=True)
    akta_cerai = models.CharField(max_length=18, blank=True, null=True)
    tgl_cerai = models.DateField(blank=True, null=True)
    kelainan_fisik = models.CharField(max_length=50, blank=True, null=True)
    foto = models.ImageField(upload_to=file_destination, blank=True, null=True)
    pass_field = models.CharField(
        db_column="pass", max_length=20, blank=True, null=True
    )  # Field renamed because it was a Python reserved word.

    def __str__(self):
        return f"{self.nama} ({self.nik})"

    class Meta(CustomModel.Meta):

        db_table = "sad_penduduk"


class SadKelahiran(CustomModel):
    nama = models.CharField(max_length=50, blank=True, null=True)
    jenis_kelamin = models.CharField(max_length=20, blank=True, null=True)
    tempat_dilahirkan = models.CharField(max_length=20, blank=True, null=True)
    tempat_kelahiran = models.CharField(max_length=20, blank=True, null=True)
    waktu_kelahiran = models.DateField(blank=True, null=True)
    jenis_kelahiran = models.CharField(max_length=20, blank=True, null=True)
    kelahiran_ke = models.CharField(max_length=5, blank=True, null=True)
    penolong_kelahiran = models.CharField(max_length=30, blank=True, null=True)
    berat_bayi = models.CharField(max_length=10, blank=True, null=True)
    panjang_bayi = models.CharField(max_length=10, blank=True, null=True)
    nik_ayah = models.CharField(max_length=16, blank=True, null=True)
    nik_ibu = models.CharField(max_length=16, blank=True, null=True)
    nama_ayah = models.CharField(max_length=50, blank=True, null=True)
    nama_ibu = models.CharField(max_length=50, blank=True, null=True)
    nama_pelapor = models.CharField(max_length=50, blank=True, null=True)
    nik_saksi_satu = models.CharField(max_length=16, blank=True, null=True)
    nik_saksi_dua = models.CharField(max_length=16, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sad_kelahiran"


class SadKematian(CustomModel):
    penduduk = models.ForeignKey(
        "SadPenduduk", models.DO_NOTHING, blank=True, null=True
    )
    tanggal_kematian = models.DateField(blank=True, null=True)
    sebab_kematian = models.CharField(max_length=50, blank=True, null=True)
    tempat_kematian = models.CharField(max_length=50, blank=True, null=True)
    yang_menerangkan = models.CharField(max_length=50, blank=True, null=True)
    nama_pelapor = models.CharField(max_length=50, blank=True, null=True)
    nama_saksi_satu = models.CharField(max_length=50, blank=True, null=True)
    nama_saksi_dua = models.CharField(max_length=50, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sad_kematian"


class SadLahirmati(CustomModel):
    lama_kandungan = models.CharField(max_length=20, blank=True, null=True)
    jenis_kelamin = models.CharField(max_length=20, blank=True, null=True)
    tanggal_lahir = models.DateField(blank=True, null=True)
    jenis_kelahiran = models.CharField(max_length=20, blank=True, null=True)
    kelahiran_ke = models.CharField(max_length=5, blank=True, null=True)
    tempat_dilahirkan = models.CharField(max_length=50, blank=True, null=True)
    penolong_kelahiran = models.CharField(max_length=50, blank=True, null=True)
    sebab_lahirmati = models.CharField(max_length=50, blank=True, null=True)
    yang_menentukan = models.CharField(max_length=50, blank=True, null=True)
    tempat_kelahiran = models.CharField(max_length=50, blank=True, null=True)
    nik_ayah = models.CharField(max_length=16, blank=True, null=True)
    nik_ibu = models.CharField(max_length=16, blank=True, null=True)
    nama_ayah = models.CharField(max_length=50, blank=True, null=True)
    nama_ibu = models.CharField(max_length=50, blank=True, null=True)
    nama_pelapor = models.CharField(max_length=50, blank=True, null=True)

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
        SadDesa, models.DO_NOTHING, blank=True, null=True
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
    alamat = models.CharField(max_length=100, blank=True, null=True)
    rt_id = models.ForeignKey(SadRt, models.DO_NOTHING, blank=True, null=True)
    nik_datang = models.CharField(max_length=128, blank=True, null=True)

    def anggota_masuk(self):
        nik_s = list(self.nik_datang.split(","))
        if nik_s:
            return SadPenduduk.all_objects.filter(pk__in=nik_s)
        return []

    class Meta(CustomModel.Meta):

        db_table = "sad_pindah_masuk"


class SadSarpras(CustomModel):
    nama_sarpras = models.CharField(max_length=100, blank=True, null=True)
    asal = models.CharField(max_length=50, blank=True, null=True)
    tgl_awal = models.DateField(blank=True, null=True)
    keadaan_awal = models.CharField(max_length=50, blank=True, null=True)
    tgl_hapus = models.DateField(blank=True, null=True)
    ket_hapus = models.CharField(max_length=50, blank=True, null=True)
    keadaan_akhir = models.CharField(max_length=50, blank=True, null=True)
    keterangan = models.TextField(blank=True, null=True)
    tahun = models.CharField(max_length=4, blank=True, null=True)
    foto = models.ImageField(upload_to=file_destination, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sad_sarpras"


class SadInventaris(CustomModel):
    nama_inventaris = models.CharField(max_length=100, blank=True, null=True)
    asal = models.CharField(max_length=50, blank=True, null=True)
    tgl_awal = models.DateField(blank=True, null=True)
    keadaan_awal = models.CharField(max_length=50, blank=True, null=True)
    tgl_hapus = models.DateField(blank=True, null=True)
    ket_hapus = models.CharField(max_length=50, blank=True, null=True)
    keadaan_akhir = models.CharField(max_length=50, blank=True, null=True)
    keterangan = models.TextField(blank=True, null=True)
    tahun = models.CharField(max_length=4, blank=True, null=True)
    foto = models.ImageField(upload_to=file_destination, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sad_inventaris"


class SadSurat(CustomModel):
    judul = models.CharField(max_length=100, blank=True, null=True)
    sifat = models.CharField(max_length=50, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sad_surat"


class SadDetailSurat(CustomModel):
    no_surat = models.CharField(max_length=50, blank=True, null=True)
    surat = models.ForeignKey(
        "SadSurat", models.DO_NOTHING, blank=True, null=True
    )
    pegawai = models.ForeignKey(
        Pegawai, models.DO_NOTHING, blank=True, null=True
    )
    lampiran = models.CharField(max_length=50, blank=True, null=True)
    keterangan = models.CharField(max_length=50, blank=True, null=True)
    tempat_tujuan = models.CharField(max_length=50, blank=True, null=True)
    pengikut_pindah = models.CharField(max_length=50, blank=True, null=True)
    asal = models.CharField(max_length=50, blank=True, null=True)
    barang_yg_hilang = models.CharField(max_length=50, blank=True, null=True)
    tgl_jam_kehilangan = models.CharField(max_length=50, blank=True, null=True)
    pelapor = models.CharField(max_length=50, blank=True, null=True)
    nama_yg_sama = models.CharField(max_length=50, blank=True, null=True)
    keperluan = models.CharField(max_length=50, blank=True, null=True)
    berlaku_mulai = models.DateField(blank=True, null=True)
    sampai_dengan = models.DateField(blank=True, null=True)
    nama_acara = models.CharField(max_length=50, blank=True, null=True)
    tgl_acara = models.DateField(blank=True, null=True)
    tempat_acara = models.CharField(max_length=50, blank=True, null=True)
    jenis_hiburan = models.CharField(max_length=50, blank=True, null=True)
    nama_grup = models.CharField(max_length=50, blank=True, null=True)
    pimpinan_acara = models.CharField(max_length=50, blank=True, null=True)
    jumlah_keluarga_yg_pindah = models.CharField(
        max_length=50, blank=True, null=True
    )
    hubungan = models.CharField(max_length=50, blank=True, null=True)
    data_penduduk_luar_desa = models.CharField(
        max_length=50, blank=True, null=True
    )

    class Meta(CustomModel.Meta):

        db_table = "sad_detail_surat"


class SettingDesa(CustomModel):
    desa = models.ForeignKey(SadDesa, models.DO_NOTHING, blank=True, null=True)
    key = models.CharField(max_length=20, blank=True, null=True)
    value = models.CharField(max_length=100, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "setting_desa"


class SigPemilik(CustomModel):
    pemilik = models.ForeignKey(
        SadPenduduk, models.DO_NOTHING, blank=True, null=True
    )
    penguasa = models.CharField(max_length=100, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sig_pemilik"


class SigBidang(CustomModel):
    nbt = models.CharField(max_length=20, blank=True, null=True)
    namabidang = models.CharField(max_length=50, blank=True, null=True)
    sig_rt = models.ForeignKey(
        "SigRt", models.DO_NOTHING, blank=True, null=True
    )
    pemilik_warga = models.ForeignKey(
        "SadPenduduk", models.DO_NOTHING, blank=True, null=True
    )
    pemilik_nonwarga = models.CharField(max_length=100, blank=True, null=True)
    penguasa = models.CharField(max_length=100, blank=True, null=True)
    geometry = JSONField(blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sig_bidang"


class SigBidang2(CustomModel):
    nbt = models.IntegerField(blank=True, null=True)
    sig_rt2 = models.ForeignKey(
        "SigRt2", models.DO_NOTHING, blank=True, null=True
    )

    class Meta(CustomModel.Meta):

        db_table = "sig_bidang2"


class SigDesa(CustomModel):
    nama_desa = models.CharField(max_length=250, blank=True, null=True)
    luas = models.CharField(max_length=10, blank=True, null=True)
    keliling = models.CharField(max_length=10, blank=True, null=True)
    geometry = JSONField(blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sig_desa"


class SigDusun(CustomModel):
    sig_desa = models.ForeignKey(
        SigDesa, models.DO_NOTHING, blank=True, null=True
    )
    nama_dusun = models.CharField(max_length=70, blank=True, null=True)
    luas = models.CharField(max_length=10, blank=True, null=True)
    keliling = models.CharField(max_length=10, blank=True, null=True)
    geometry = JSONField(blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sig_dusun"


class SigDukuh(CustomModel):
    sig_dusun = models.ForeignKey(
        SigDusun, models.DO_NOTHING, blank=True, null=True
    )
    nama_dukuh = models.CharField(max_length=70, blank=True, null=True)
    luas = models.CharField(max_length=10, blank=True, null=True)
    keliling = models.CharField(max_length=10, blank=True, null=True)
    geometry = JSONField(blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sig_dukuh"


class SigDukuh2(CustomModel):
    sig_desa = models.ForeignKey(
        SigDesa, models.DO_NOTHING, blank=True, null=True
    )
    nama_dukuh = models.CharField(max_length=70, blank=True, null=True)
    luas = models.CharField(max_length=10, blank=True, null=True)
    keliling = models.CharField(max_length=10, blank=True, null=True)
    geometry = JSONField(blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sig_dukuh2"


class SigRw(CustomModel):
    sig_dukuh = models.ForeignKey(
        SigDukuh, models.DO_NOTHING, blank=True, null=True
    )
    rw = models.CharField(max_length=10, blank=True, null=True)
    geometry = JSONField(blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sig_rw"


class SigRt(CustomModel):
    sig_rw = models.ForeignKey(
        "SigRw", models.DO_NOTHING, blank=True, null=True
    )
    rt = models.CharField(max_length=10, blank=True, null=True)
    geometry = JSONField(blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sig_rt"


class SigRw2(CustomModel):
    sig_dukuh2 = models.ForeignKey(
        SigDukuh2, models.DO_NOTHING, blank=True, null=True
    )
    rw = models.CharField(max_length=10, blank=True, null=True)
    geometry = JSONField(blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sig_rw2"


class SigRt2(CustomModel):
    sig_rw2 = models.ForeignKey(
        "SigRw2", models.DO_NOTHING, blank=True, null=True
    )
    rt = models.CharField(max_length=10, blank=True, null=True)
    geometry = JSONField(blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sig_rt2"


class SigSadDesa(CustomModel):
    sad_desa = models.ForeignKey(
        SadDesa, models.DO_NOTHING, blank=True, null=True
    )
    sig_desa = models.ForeignKey(
        SigDesa, models.DO_NOTHING, blank=True, null=True
    )

    class Meta(CustomModel.Meta):

        db_table = "sig_sad_desa"


class SigSadBidang(CustomModel):
    sad_penduduk = models.ForeignKey(
        SadPenduduk, models.DO_NOTHING, blank=True, null=True
    )
    sig_bidang = models.ForeignKey(
        SigBidang, models.DO_NOTHING, blank=True, null=True
    )
    pemilik = models.CharField(max_length=100, blank=True, null=True)
    penguasa = models.CharField(max_length=100, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sig_sad_bidang"


class SigSadBidang2(CustomModel):
    sad_penduduk = models.ForeignKey(
        SadPenduduk, models.DO_NOTHING, blank=True, null=True
    )
    sig_bidang2 = models.ForeignKey(
        SigBidang2, models.DO_NOTHING, blank=True, null=True
    )
    pemilik = models.CharField(max_length=100, blank=True, null=True)
    penguasa = models.CharField(max_length=100, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sig_sad_bidang2"


class Slider(CustomModel):
    judul = models.CharField(max_length=100, blank=True, null=True)
    deskripsi = models.TextField(blank=True, null=True)
    gambar = models.ImageField(
        upload_to=file_destination, blank=True, null=True
    )

    class Meta(CustomModel.Meta):

        db_table = "slider"


class KategoriArtikel(models.Model):
    nama = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nama

    class Meta:

        db_table = "KategoriArtikel"


class Artikel(models.Model):
    kategori = models.ForeignKey(
        KategoriArtikel, models.DO_NOTHING, blank=True, null=True
    )
    tgl = models.DateField(blank=True, null=True)
    judul = models.CharField(max_length=100, blank=True, null=True)
    isi = models.TextField(blank=True, null=True)
    gambar = models.ImageField(
        upload_to=file_destination, blank=True, null=True
    )

    class Meta:

        db_table = "Artikel"


class KategoriPotensi(models.Model):
    nama = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nama

    class Meta:
        db_table = "KategoriPotensi"


class Potensi(models.Model):
    kategori = models.ForeignKey(
        KategoriPotensi, models.DO_NOTHING, blank=True, null=True
    )
    bidang = models.CharField(max_length=100, blank=True, null=True)
    judul = models.CharField(max_length=100, blank=True, null=True)
    harga = models.CharField(max_length=100, blank=True, null=True)
    isi = models.TextField(blank=True, null=True)
    geometry = models.TextField(blank=True, null=True)
    centroid = models.TextField(blank=True, null=True)
    gambar = models.ImageField(
        upload_to=file_destination, blank=True, null=True
    )

    class Meta:

        db_table = "Potensi"


class KategoriInformasi(models.Model):
    nama = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nama

    class Meta:

        db_table = "KategoriInformasi"


class Informasi(models.Model):
    kategori = models.ForeignKey(
        KategoriInformasi, models.DO_NOTHING, blank=True, null=True
    )
    judul = models.CharField(max_length=100, blank=True, null=True)
    tempat = models.CharField(max_length=100, blank=True, null=True)
    tanggal = models.DateField(blank=True, null=True)
    mulai = models.CharField(max_length=10, blank=True, null=True)
    selesai = models.CharField(max_length=10, blank=True, null=True)
    gambar = models.ImageField(
        upload_to=file_destination, blank=True, null=True
    )

    class Meta:

        db_table = "Informasi"


class KategoriLapor(models.Model):
    nama = models.CharField(max_length=100, blank=True, null=True)
    gambar = models.ImageField(
        upload_to=file_destination, blank=True, null=True
    )

    def __str__(self):
        return self.nama

    class Meta:

        db_table = "KategoriLapor"


class Lapor(models.Model):
    kategori = models.ForeignKey(
        KategoriLapor, models.DO_NOTHING, blank=True, null=True
    )
    judul = models.CharField(max_length=100, blank=True, null=True)
    isi = models.TextField(blank=True, null=True)
    gambar = models.ImageField(
        upload_to=file_destination, blank=True, null=True
    )

    class Meta:

        db_table = "Lapor"


class SuratDomisili(CustomModel):
    no_surat = models.CharField(max_length=50, blank=True, null=True)
    pegawai = models.ForeignKey(
        Pegawai, models.DO_NOTHING, blank=True, null=True
    )
    penduduk = models.ForeignKey(
        SadPenduduk, models.DO_NOTHING, blank=True, null=True
    )
    keperluan = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "surat_domisili"


class SuratSkck(CustomModel):
    no_surat = models.CharField(max_length=50, blank=True, null=True)
    pegawai = models.ForeignKey(
        Pegawai, models.DO_NOTHING, blank=True, null=True
    )
    penduduk = models.ForeignKey(
        SadPenduduk, models.DO_NOTHING, blank=True, null=True
    )
    keterangan = models.TextField(blank=True, null=True)
    keperluan = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "surat_skck"


class SuratKelahiran(CustomModel):
    no_surat = models.CharField(max_length=50, blank=True, null=True)
    pegawai = models.ForeignKey(
        Pegawai,
        models.DO_NOTHING,
        related_name="acc_surat_kelahiran",
        blank=True,
        null=True,
    )
    ayah = models.ForeignKey(
        SadPenduduk,
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="ayah_surat_lahir",
    )
    ibu = models.ForeignKey(
        SadPenduduk,
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="ibu_surat_lahir",
    )
    saksi1 = models.ForeignKey(
        SadPenduduk,
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="saksi1_surat_lahir",
    )
    saksi2 = models.ForeignKey(
        SadPenduduk,
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="saksi2_surat_lahir",
    )
    nama = models.CharField(max_length=100, blank=True, null=True)
    jk = models.CharField(max_length=15, blank=True, null=True)
    tempat_dilahirkan = models.CharField(max_length=50, blank=True, null=True)
    tempat_kelahiran = models.CharField(max_length=50, blank=True, null=True)
    tgl = models.DateField(blank=True, null=True)
    jenis_kelahiran = models.CharField(max_length=15, blank=True, null=True)
    kelahiran_ke = models.CharField(max_length=15, blank=True, null=True)
    penolong_kelahiran = models.CharField(max_length=15, blank=True, null=True)
    berat = models.CharField(max_length=15, blank=True, null=True)
    panjang = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        db_table = "surat_kelahiran"
