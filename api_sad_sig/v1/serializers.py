from django.contrib.auth.models import User, Group
from dynamic_rest.serializers import DynamicModelSerializer
from dynamic_rest.fields import DynamicRelationField
from rest_framework import serializers
from .models import (
  Pegawai,
  SadProvinsi,
  SadKabKota,
  SadKecamatan,
  SadDesa,
  SadDusunDukuh,
  SadRw,
  SadRt,
  SadKeluarga,
  SadPenduduk,
  SadKelahiran,
  SadKematian,
  SadLahirmati,
  SadPindahKeluar,
  SadPindahMasuk,
  SadSarpras,
  SadInventaris,
  SadSurat,
  SadDetailSurat,
  SigBidang,
  SigDesa,
  SigDusunDukuh,
  SigRt,
  SigRw,
  SigSadDesa,
  SigSadDusunDukuh,
  SigSadRw,
  SigSadRt,
)

class GroupSerializer(DynamicModelSerializer):
  class Meta:
    model = Group
    name = 'data'
    fields = ['id', 'name']


class UserSerializer(DynamicModelSerializer):
  # group = DynamicRelationField('GroupSerializer', deferred=False, embed=True)
  class Meta:
    model = User
    name = 'data'
    exclude = []
  
  def create(self, validated_data):
    user = super().create(validated_data)
    user.is_active = True
    user.set_password(validated_data['password'])
    user.save()

    return user

  def update(self, instance, validated_data):
    user = super().update(instance, validated_data)
    user.set_password(validated_data['password'])
    user.save()

    return user



class PegawaiSerializer(DynamicModelSerializer):
  class Meta:
    model = Pegawai
    name = 'data'
    fields = ['id', 'nama', 'jabatan']

class SadProvinsiSerializer(DynamicModelSerializer):
  class Meta:
    model = SadProvinsi
    name = 'data'
    fields = ['id', 'kode_provinsi', 'nama_provinsi']

class SadKabKotaSerializer(DynamicModelSerializer):
  class Meta:
    model = SadKabKota
    name = 'data'
    fields = ['id', 'kode_kab_kota', 'nama_kab_kota']

class SadKecamatanSerializer(DynamicModelSerializer):
  kab_kota = DynamicRelationField('SadKabKotaSerializer', deferred=False, embed=True)
  class Meta:
    model = SadKecamatan
    name = 'data'
    fields = ['id', 'kode_kecamatan', 'nama_kecamatan', 'kab_kota']
  
class SadDesaSerializer(DynamicModelSerializer):
  kecamatan = DynamicRelationField('SadKecamatanSerializer', deferred=False, embed=True)
  class Meta:
    model = SadDesa
    name = 'data'
    fields = ['id', 'kode_desa', 'nama_desa', 'kecamatan']

class SadDusunDukuhSerializer(DynamicModelSerializer):
  class Meta:
    model = SadDusunDukuh
    name = 'data'
    fields = ['id', 'nama']

class SadRwSerializer(DynamicModelSerializer):
  class Meta:
    model = SadRw
    name = 'data'
    fields = ['id', 'rw']

class SadRtSerializer(DynamicModelSerializer):
  class Meta:
    model = SadRt
    name = 'data'
    fields = ['id', 'rt']

class SadKeluargaSerializer(DynamicModelSerializer):
  anggota = DynamicRelationField('SadPendudukSerializer', many=True, deferred=True, embed=True)
  class Meta:
    model = SadKeluarga
    name = 'data'
    exclude = []
    extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

class SadPendudukSerializer(DynamicModelSerializer):
  keluarga = DynamicRelationField('SadKeluargaSerializer', deferred=True, embed=True)
  class Meta:
    model = SadPenduduk
    name = 'data'
    exclude = []

class SadKelahiranSerializer(DynamicModelSerializer):
  class Meta:
    model = SadKelahiran
    name = 'data'
    fields = ['id', 'nama', 'jenis_kelamin']

class SadKematianSerializer(DynamicModelSerializer):
  class Meta:
    model = SadKematian
    name = 'data'
    fields = ['id', 'tanggal_kematian', 'sebab_kematian']

class SadLahirmatiSerializer(DynamicModelSerializer):
  class Meta:
    model = SadLahirmati
    name = 'data'
    fields = ['id', 'lama_kandungan', 'jenis_kelamin']

class SadPindahKeluarSerializer(DynamicModelSerializer):
  class Meta:
    model = SadPindahKeluar
    name = 'data'
    fields = ['id', 'pemohon', 'alasan']

class SadPindahMasukSerializer(DynamicModelSerializer):
  class Meta:
    model = SadPindahMasuk
    name = 'data'
    fields = ['id', 'no_kk', 'nik_kepala_keluarga']

class SadSarprasSerializer(DynamicModelSerializer):
  class Meta:
    model = SadSarpras
    name = 'data'
    fields = ['id', 'nama_sarpras', 'asal']

class SadInventarisSerializer(DynamicModelSerializer):
  class Meta:
    model = SadInventaris
    name = 'data'
    fields = ['id', 'nama_inventaris', 'asal']

class SadSuratSerializer(DynamicModelSerializer):
  class Meta:
    model = SadSurat
    name = 'data'
    fields = ['id', 'judul', 'sifat']

class SadDetailSuratSerializer(DynamicModelSerializer):
  class Meta:
    model = SadDetailSurat
    name = 'data'
    fields = ['id', 'no_surat', 'keterangan']

class SigBidangSerializer(DynamicModelSerializer):
  class Meta:
    model = SigBidang
    name = 'data'
    exclude = []

class SigDesaSerializer(DynamicModelSerializer):
  class Meta:
    model = SigDesa
    name = 'data'
    exclude = []

class SigDusunDukuhSerializer(DynamicModelSerializer):
  sig_desa = DynamicRelationField('SigDesaSerializer', deferred=True, embed=True)
  class Meta:
    model = SigDusunDukuh
    name = 'data'
    exclude = []

class SigRtSerializer(DynamicModelSerializer):
  class Meta:
    model = SigRt
    name = 'data'
    exclude = []

class SigRwSerializer(DynamicModelSerializer):
  class Meta:
    model = SigRw
    name = 'data'
    exclude = []

class SigSadDesaSerializer(DynamicModelSerializer):
  class Meta:
    model = SigSadDesa
    name = 'data'
    exclude = []

class SigSadDusunDukuhSerializer(DynamicModelSerializer):
  class Meta:
    model = SigSadDusunDukuh
    name = 'data'
    exclude = []

class SigSadRwSerializer(DynamicModelSerializer):
  class Meta:
    model = SigSadRw
    name = 'data'
    exclude = []

class SigSadRtSerializer(DynamicModelSerializer):
  class Meta:
    model = SigSadRt
    name = 'data'
    exclude = []