from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

# Create your models here.


class Pegawai(models.Model):
    nip = models.CharField(max_length=18, blank=True, null=True)
    nama = models.CharField(max_length=50, blank=True, null=True)
    jabatan = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(max_length=30, blank=True, null=True)
    golongan = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = "pegawai"


class SadProvinsi(models.Model):
    kode_provinsi = models.CharField(max_length=5, blank=True, null=True)
    nama_provinsi = models.CharField(max_length=50, blank=True, null=True)

    class Meta:

        db_table = "sad_provinsi"


class SadKabKota(models.Model):
    provinsi = models.ForeignKey(
        "SadProvinsi", models.DO_NOTHING, blank=True, null=True
    )
    kode_kab_kota = models.CharField(max_length=5, blank=True, null=True)
    nama_kab_kota = models.CharField(max_length=50, blank=True, null=True)

    class Meta:

        db_table = "sad_kab_kota"


class SadKecamatan(models.Model):
    kab_kota = models.ForeignKey(
        SadKabKota, models.DO_NOTHING, blank=True, null=True
    )
    kode_kecamatan = models.CharField(max_length=5, blank=True, null=True)
    nama_kecamatan = models.CharField(max_length=250, blank=True, null=True)

    class Meta:

        db_table = "sad_kecamatan"


class SadDesa(models.Model):
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
    logo = models.TextField(blank=True, null=True)

    class Meta:

        db_table = "sad_desa"


class SadDusunDukuh(models.Model):
    desa_id = models.IntegerField(blank=True, null=True)
    tipe = models.CharField(max_length=5, blank=True, null=True)
    nama = models.CharField(max_length=70, blank=True, null=True)
    dusun_dukuh = models.ForeignKey(
        "self", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:

        db_table = "sad_dusun_dukuh"


class SadRt(models.Model):
    rw = models.ForeignKey("SadRw", models.DO_NOTHING, blank=True, null=True)
    rt = models.CharField(max_length=10, blank=True, null=True)

    class Meta:

        db_table = "sad_rt"


class SadRw(models.Model):
    dusun_dukuh = models.ForeignKey(
        SadDusunDukuh, models.DO_NOTHING, blank=True, null=True
    )
    desa_id = models.IntegerField(blank=True, null=True)
    rw = models.CharField(max_length=10, blank=True, null=True)

    class Meta:

        db_table = "sad_rw"


class SadKeluarga(models.Model):
    no_kk = models.CharField(max_length=16, blank=True, null=True)
    alamat = models.CharField(max_length=100, blank=True, null=True)
    rt = models.ForeignKey("SadRt", models.DO_NOTHING, blank=True, null=True)
    kode_pos = models.CharField(max_length=5, blank=True, null=True)
    status_kesejahteraan = models.CharField(
        max_length=30, blank=True, null=True
    )
    penghasil = models.IntegerField(blank=True, null=True)
    status_kk = models.CharField(max_length=20, blank=True, null=True)
    created_by = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="created_by",
        blank=True,
        null=True,
        related_name="keluarga_create_by",
    )
    created_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="updated_by",
        blank=True,
        null=True,
        related_name="keluarga_update_by",
    )
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="deleted_by",
        blank=True,
        null=True,
        related_name="keluarga_delete_by",
    )
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = "sad_keluarga"


class SadPenduduk(models.Model):
    keluarga = models.ForeignKey(
        SadKeluarga,
        models.DO_NOTHING,
        related_name="anggota",
        blank=True,
        null=True,
    )
    nik = models.CharField(max_length=16, blank=True, null=True)
    chip_ektp = models.CharField(max_length=10, blank=True, null=True)
    nama = models.CharField(max_length=50, blank=True, null=True)
    tgl_lahir = models.DateField(blank=True, null=True)
    tempat_lahir = models.CharField(max_length=50, blank=True, null=True)
    jk = models.CharField(max_length=12, blank=True, null=True)
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
    foto = models.CharField(max_length=50, blank=True, null=True)
    pass_field = models.CharField(
        db_column="pass", max_length=20, blank=True, null=True
    )  # Field renamed because it was a Python reserved word.

    class Meta:

        db_table = "sad_penduduk"


class SadKelahiran(models.Model):
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
    # created_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='created_by', blank=True, null=True)
    # created_at = models.DateTimeField(blank=True, null=True)
    # updated_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='updated_by', blank=True, null=True)
    # updated_at = models.DateTimeField(blank=True, null=True)
    # deleted_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='deleted_by', blank=True, null=True)
    # deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = "sad_kelahiran"


class SadKematian(models.Model):
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
    # created_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='created_by', blank=True, null=True)
    # created_at = models.DateTimeField(blank=True, null=True)
    # updated_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='updated_by', blank=True, null=True)
    # updated_at = models.DateTimeField(blank=True, null=True)
    # deleted_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='deleted_by', blank=True, null=True)
    # deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = "sad_kematian"


class SadLahirmati(models.Model):
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
    # created_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='created_by', blank=True, null=True)
    # created_at = models.DateTimeField(blank=True, null=True)
    # updated_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='updated_by', blank=True, null=True)
    # updated_at = models.DateTimeField(blank=True, null=True)
    # deleted_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='deleted_by', blank=True, null=True)
    # deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = "sad_lahirmati"


class SadPindahKeluar(models.Model):
    keluarga = models.ForeignKey(
        SadKeluarga, models.DO_NOTHING, blank=True, null=True
    )
    pemohon = models.CharField(max_length=30, blank=True, null=True)
    alasan = models.CharField(max_length=100, blank=True, null=True)
    provinsi_tujuan = models.CharField(max_length=20, blank=True, null=True)
    kota_tujuan = models.CharField(max_length=20, blank=True, null=True)
    kecamatan_tujuan = models.CharField(max_length=20, blank=True, null=True)
    kelurahan_tujuan = models.CharField(max_length=20, blank=True, null=True)
    dusun_tujuan = models.CharField(max_length=20, blank=True, null=True)
    rt_tujuan = models.CharField(max_length=5, blank=True, null=True)
    rw_tujuan = models.CharField(max_length=5, blank=True, null=True)
    kodepos_tujuan = models.CharField(max_length=5, blank=True, null=True)
    no_telp = models.CharField(max_length=13, blank=True, null=True)
    klarifikasi_pindah = models.CharField(max_length=50, blank=True, null=True)
    jenis_kepindahan = models.CharField(max_length=50, blank=True, null=True)
    status_no_kk_pindah = models.CharField(
        max_length=50, blank=True, null=True
    )
    rencana_tgl_pindah = models.DateField(blank=True, null=True)
    # created_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='created_by', blank=True, null=True)
    # created_at = models.DateTimeField(blank=True, null=True)
    # updated_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='updated_by', blank=True, null=True)
    # updated_at = models.DateTimeField(blank=True, null=True)
    # deleted_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='deleted_by', blank=True, null=True)
    # deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = "sad_pindah_keluar"


class SadPindahMasuk(models.Model):
    no_kk = models.CharField(max_length=18, blank=True, null=True)
    status_no_kk_pindah = models.CharField(
        max_length=20, blank=True, null=True
    )
    tanggal_kedatangan = models.DateField(blank=True, null=True)
    alamat = models.CharField(max_length=100, blank=True, null=True)
    rt_id = models.IntegerField(blank=True, null=True)
    yang_datang = models.TextField(blank=True, null=True)
    # created_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='created_by', blank=True, null=True)
    # created_at = models.DateTimeField(blank=True, null=True)
    # updated_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='updated_by', blank=True, null=True)
    # updated_at = models.DateTimeField(blank=True, null=True)
    # deleted_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='deleted_by', blank=True, null=True)
    # deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = "sad_pindah_masuk"


class SadSarpras(models.Model):
    nama_sarpras = models.CharField(max_length=100, blank=True, null=True)
    asal = models.CharField(max_length=50, blank=True, null=True)
    tgl_awal = models.DateField(blank=True, null=True)
    keadaan_awal = models.CharField(max_length=50, blank=True, null=True)
    tgl_hapus = models.DateField(blank=True, null=True)
    ket_hapus = models.CharField(max_length=50, blank=True, null=True)
    keadaan_akhir = models.CharField(max_length=50, blank=True, null=True)
    keterangan = models.TextField(blank=True, null=True)
    tahun = models.CharField(max_length=4, blank=True, null=True)
    foto = models.CharField(max_length=200, blank=True, null=True)
    # created_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='created_by', blank=True, null=True)
    # created_at = models.DateTimeField(blank=True, null=True)
    # updated_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='updated_by', blank=True, null=True)
    # updated_at = models.DateTimeField(blank=True, null=True)
    # deleted_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='deleted_by', blank=True, null=True)
    # deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = "sad_sarpras"


class SadInventaris(models.Model):
    nama_inventaris = models.CharField(max_length=100, blank=True, null=True)
    asal = models.CharField(max_length=50, blank=True, null=True)
    tgl_awal = models.DateField(blank=True, null=True)
    keadaan_awal = models.CharField(max_length=50, blank=True, null=True)
    tgl_hapus = models.DateField(blank=True, null=True)
    ket_hapus = models.CharField(max_length=50, blank=True, null=True)
    keadaan_akhir = models.CharField(max_length=50, blank=True, null=True)
    keterangan = models.TextField(blank=True, null=True)
    tahun = models.CharField(max_length=4, blank=True, null=True)
    foto = models.CharField(max_length=200, blank=True, null=True)
    # created_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='created_by', blank=True, null=True)
    # created_at = models.DateTimeField(blank=True, null=True)
    # updated_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='updated_by', blank=True, null=True)
    # updated_at = models.DateTimeField(blank=True, null=True)
    # deleted_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='deleted_by', blank=True, null=True)
    # deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = "sad_inventaris"


class SadSurat(models.Model):
    judul = models.CharField(max_length=100, blank=True, null=True)
    sifat = models.CharField(max_length=50, blank=True, null=True)
    # created_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='created_by', blank=True, null=True)
    # created_at = models.DateTimeField(blank=True, null=True)
    # updated_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='updated_by', blank=True, null=True)
    # updated_at = models.DateTimeField(blank=True, null=True)
    # deleted_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='deleted_by', blank=True, null=True)
    # deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = "sad_surat"


class SadDetailSurat(models.Model):
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
    # created_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='created_by', blank=True, null=True)
    # created_at = models.DateTimeField(blank=True, null=True)
    # updated_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='updated_by', blank=True, null=True)
    # updated_at = models.DateTimeField(blank=True, null=True)
    # deleted_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='deleted_by', blank=True, null=True)
    # deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = "sad_detail_surat"


class SettingDesa(models.Model):
    desa = models.ForeignKey(SadDesa, models.DO_NOTHING, blank=True, null=True)
    key = models.CharField(max_length=20, blank=True, null=True)
    value = models.CharField(max_length=100, blank=True, null=True)

    class Meta:

        db_table = "setting_desa"


class SigBidang(models.Model):
    nbt = models.IntegerField(blank=True, null=True)
    sig_rt = models.ForeignKey(
        "SigRt", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:

        db_table = "sig_bidang"


class SigBidang2(models.Model):
    nbt = models.IntegerField(blank=True, null=True)
    sig_rt2 = models.ForeignKey(
        "SigRt2", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:

        db_table = "sig_bidang2"


class SigDesa(models.Model):
    nama_desa = models.CharField(max_length=250, blank=True, null=True)
    luas = models.CharField(max_length=10, blank=True, null=True)
    keliling = models.CharField(max_length=10, blank=True, null=True)
    geometry = JSONField(blank=True, null=True)

    class Meta:

        db_table = "sig_desa"


class SigDusun(models.Model):
    sig_desa = models.ForeignKey(
        SigDesa, models.DO_NOTHING, blank=True, null=True
    )
    nama_dusun = models.CharField(max_length=70, blank=True, null=True)
    luas = models.CharField(max_length=10, blank=True, null=True)
    keliling = models.CharField(max_length=10, blank=True, null=True)
    geometry = JSONField(blank=True, null=True)

    class Meta:

        db_table = "sig_dusun"


class SigDukuh(models.Model):
    sig_dusun = models.ForeignKey(
        SigDusun, models.DO_NOTHING, blank=True, null=True
    )
    nama_dukuh = models.CharField(max_length=70, blank=True, null=True)
    luas = models.CharField(max_length=10, blank=True, null=True)
    keliling = models.CharField(max_length=10, blank=True, null=True)
    geometry = JSONField(blank=True, null=True)

    class Meta:

        db_table = "sig_dukuh"


class SigDukuh2(models.Model):
    sig_desa = models.ForeignKey(
        SigDesa, models.DO_NOTHING, blank=True, null=True
    )
    nama_dukuh = models.CharField(max_length=70, blank=True, null=True)
    luas = models.CharField(max_length=10, blank=True, null=True)
    keliling = models.CharField(max_length=10, blank=True, null=True)
    geometry = JSONField(blank=True, null=True)

    class Meta:

        db_table = "sig_dukuh2"


class SigRw(models.Model):
    sig_dukuh = models.ForeignKey(
        SigDukuh, models.DO_NOTHING, blank=True, null=True
    )
    rw = models.CharField(max_length=10, blank=True, null=True)
    geometry = JSONField(blank=True, null=True)

    class Meta:

        db_table = "sig_rw"


class SigRt(models.Model):
    sig_rw = models.ForeignKey(
        "SigRw", models.DO_NOTHING, blank=True, null=True
    )
    rt = models.CharField(max_length=10, blank=True, null=True)
    geometry = JSONField(blank=True, null=True)

    class Meta:

        db_table = "sig_rt"


class SigRw2(models.Model):
    sig_dukuh2 = models.ForeignKey(
        SigDukuh2, models.DO_NOTHING, blank=True, null=True
    )
    rw = models.CharField(max_length=10, blank=True, null=True)
    geometry = JSONField(blank=True, null=True)

    class Meta:

        db_table = "sig_rw2"


class SigRt2(models.Model):
    sig_rw2 = models.ForeignKey(
        "SigRw2", models.DO_NOTHING, blank=True, null=True
    )
    rt = models.CharField(max_length=10, blank=True, null=True)
    geometry = JSONField(blank=True, null=True)

    class Meta:

        db_table = "sig_rt2"


class SigSadDesa(models.Model):
    sad_desa = models.ForeignKey(
        SadDesa, models.DO_NOTHING, blank=True, null=True
    )
    sig_desa = models.ForeignKey(
        SigDesa, models.DO_NOTHING, blank=True, null=True
    )

    class Meta:

        db_table = "sig_sad_desa"


class SigSadBidang(models.Model):
    sad_penduduk = models.ForeignKey(
        SadPenduduk, models.DO_NOTHING, blank=True, null=True
    )
    sig_bidang = models.ForeignKey(
        SigBidang, models.DO_NOTHING, blank=True, null=True
    )
    pemilik = models.CharField(max_length=100, blank=True, null=True)
    penguasa = models.CharField(max_length=100, blank=True, null=True)

    class Meta:

        db_table = "sig_sad_bidang"


class SigSadBidang2(models.Model):
    sad_penduduk = models.ForeignKey(
        SadPenduduk, models.DO_NOTHING, blank=True, null=True
    )
    sig_bidang2 = models.ForeignKey(
        SigBidang2, models.DO_NOTHING, blank=True, null=True
    )
    pemilik = models.CharField(max_length=100, blank=True, null=True)
    penguasa = models.CharField(max_length=100, blank=True, null=True)

    class Meta:

        db_table = "sig_sad_bidang2"


class Slider(models.Model):
    judul = models.CharField(max_length=100, blank=True, null=True)
    deskripsi = models.TextField(blank=True, null=True)
    gambar = models.BinaryField(blank=True, null=True)

    class Meta:

        db_table = "slider"
