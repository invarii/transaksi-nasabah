from django.contrib.auth.models import User, Group
from rest_framework.serializers import HyperlinkedModelSerializer
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
)

class UserSerializer(HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ['url', 'id', 'username', 'email', 'groups']

class GroupSerializer(HyperlinkedModelSerializer):
  class Meta:
    model = Group
    fields = ['url', 'id', 'name']

class PegawaiSerializer(HyperlinkedModelSerializer):
  class Meta:
    model = Pegawai
    fields = ['url', 'id', 'nama', 'jabatan']

class SadProvinsiSerializer(HyperlinkedModelSerializer):
  class Meta:
    model = SadProvinsi
    fields = ['url', 'id', 'kode_provinsi', 'nama_provinsi']

class SadKabKotaSerializer(HyperlinkedModelSerializer):
  class Meta:
    model = SadKabKota
    fields = ['url', 'id', 'kode_kab_kota', 'nama_kab_kota']

class SadKecamatanSerializer(HyperlinkedModelSerializer):
  class Meta:
    model = SadKecamatan
    fields = ['url', 'id', 'kode_kecamatan', 'nama_kecamatan']
  
class SadDesaSerializer(HyperlinkedModelSerializer):
  class Meta:
    model = SadDesa
    fields = ['url', 'id', 'kode_desa', 'nama_desa']

class SadDusunDukuhSerializer(HyperlinkedModelSerializer):
  class Meta:
    model = SadDusunDukuh
    fields = ['url', 'id', 'nama']

class SadRwSerializer(HyperlinkedModelSerializer):
  class Meta:
    model = SadRw
    fields = ['url', 'id', 'rw']

class SadRtSerializer(HyperlinkedModelSerializer):
  class Meta:
    model = SadRt
    fields = ['url', 'id', 'rt']

class SadKeluargaSerializer(HyperlinkedModelSerializer):
  class Meta:
    model = SadKeluarga
    fields = ['url', 'id', 'no_kk']

class SadPendudukSerializer(HyperlinkedModelSerializer):
  class Meta:
    model = SadPenduduk
    fields = ['url', 'id', 'nik', 'nama']