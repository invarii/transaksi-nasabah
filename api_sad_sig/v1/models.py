from django.db import models

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
        managed = False
        db_table = 'pegawai'

class SadProvinsi(models.Model):
    kode_provinsi = models.CharField(max_length=5, blank=True, null=True)
    nama_provinsi = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sad_provinsi'

class SadKabKota(models.Model):
    provinsi = models.ForeignKey('SadProvinsi', models.DO_NOTHING, blank=True, null=True)
    kode_kab_kota = models.CharField(max_length=5, blank=True, null=True)
    nama_kab_kota = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sad_kab_kota'

class SadKecamatan(models.Model):
    kab_kota = models.ForeignKey(SadKabKota, models.DO_NOTHING, blank=True, null=True)
    kode_kecamatan = models.CharField(max_length=5, blank=True, null=True)
    nama_kecamatan = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sad_kecamatan'

class SadDesa(models.Model):
    kecamatan = models.ForeignKey('SadKecamatan', models.DO_NOTHING, blank=True, null=True)
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
        managed = False
        db_table = 'sad_desa'

class SadDusunDukuh(models.Model):
    desa_id = models.IntegerField(blank=True, null=True)
    tipe = models.CharField(max_length=5, blank=True, null=True)
    nama = models.CharField(max_length=70, blank=True, null=True)
    dusun_dukuh = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sad_dusun_dukuh'

class SadRt(models.Model):
    rw = models.ForeignKey('SadRw', models.DO_NOTHING, blank=True, null=True)
    rt = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sad_rt'


class SadRw(models.Model):
    dusun_dukuh = models.ForeignKey(SadDusunDukuh, models.DO_NOTHING, blank=True, null=True)
    desa_id = models.IntegerField(blank=True, null=True)
    rw = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sad_rw'

class SadKeluarga(models.Model):
    no_kk = models.CharField(max_length=16, blank=True, null=True)
    alamat = models.CharField(max_length=100, blank=True, null=True)
    rt = models.ForeignKey('SadRt', models.DO_NOTHING, blank=True, null=True)
    kode_pos = models.CharField(max_length=5, blank=True, null=True)
    status_kesejahteraan = models.CharField(max_length=30, blank=True, null=True)
    penghasil = models.IntegerField(blank=True, null=True)
    status_kk = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sad_keluarga'


class SadPenduduk(models.Model):
    keluarga = models.ForeignKey(SadKeluarga, models.DO_NOTHING, related_name='anggota', blank=True, null=True)
    nik = models.CharField(max_length=16, blank=True, null=True)
    chip_ektp = models.CharField(max_length=10, blank=True, null=True)
    nama = models.CharField(max_length=50, blank=True, null=True)
    tgl_lahir = models.DateField(blank=True, null=True)
    tempat_lahir = models.CharField(max_length=50, blank=True, null=True)
    jk = models.CharField(max_length=10, blank=True, null=True)
    agama = models.CharField(max_length=20, blank=True, null=True)
    pendidikan = models.CharField(max_length=20, blank=True, null=True)
    pekerjaan = models.CharField(max_length=50, blank=True, null=True)
    status_kawin = models.CharField(max_length=20, blank=True, null=True)
    status_penduduk = models.CharField(max_length=20, blank=True, null=True)
    kewarganegaraan = models.CharField(max_length=5, blank=True, null=True)
    anak_ke = models.CharField(max_length=5, blank=True, null=True)
    golongan_darah = models.CharField(max_length=5, blank=True, null=True)
    status_dalam_keluarga = models.CharField(max_length=20, blank=True, null=True)
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
    foto = models.BinaryField(blank=True, null=True)
    pass_field = models.CharField(db_column='pass', max_length=20, blank=True, null=True)  # Field renamed because it was a Python reserved word.

    class Meta:
        managed = False
        db_table = 'sad_penduduk'
