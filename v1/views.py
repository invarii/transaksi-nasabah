import pandas
import json
from io import BytesIO
import numpy as np

from rest_framework import permissions
from django.conf import settings
from django.db.utils import IntegrityError
from django.db.models import F, Count, Avg, Sum
from django.http import HttpResponse
from dynamic_rest.viewsets import DynamicModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters, viewsets
from rest_framework.exceptions import NotFound, APIException
import pytz
from datetime import datetime
from openpyxl import Workbook
from rest_framework.permissions import AllowAny



from api_sad_sig.util import (
        CustomView,
        create_or_reactivate,
        create_or_reactivate_user,
        )
from users.permissions import IsAdminUserOrReadOnly
from .serializers import *
from .models import *


def format_data_penduduk(data):
    cols = [
            "tgl_lahir",
            "tgl_exp_paspor",
            "tgl_kawin",
            "tgl_cerai",
            ]
    for col in cols:
        if type(data[col]) == pandas.Timestamp:
            data[col] = str(data[col]).split(" ")[0]
        else:
            data.pop(col)


class SadProvinsiViewSet(CustomView):
    queryset = SadProvinsi.objects.all()
    serializer_class = SadProvinsiSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ["id", "nama_provinsi"]


class PegawaiViewSet(CustomView):
    queryset = Pegawai.objects.all().order_by("id")
    serializer_class = PegawaiSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BatasDesaViewSet(CustomView):
    queryset = BatasDesa.objects.all().order_by("id")
    serializer_class = BatasDesaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ["utara", "selatan", "timur", "barat"]


class SadKabKotaViewSet(CustomView):
    queryset = SadKabKota.objects.all().order_by("id")
    serializer_class = SadKabKotaSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get_queryset(self):
        provinsi = self.request.query_params.get("provinsi")
        if provinsi:
            return (
                    SadKabKota.objects.all()
                    .filter(provinsi_id=provinsi)
                    .order_by("nama_kab_kota")
                    )
            return SadKabKota.objects.all()


class SadKecamatanViewSet(CustomView):
    queryset = SadKecamatan.objects.all().order_by("id")
    serializer_class = SadKecamatanSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get_queryset(self):
        kabkota = self.request.query_params.get("kabkota")
        if kabkota:
            return SadKecamatan.objects.filter(kab_kota_id=kabkota).all()
        return SadKecamatan.objects.all()


class SadDesaViewSet(CustomView):
    queryset = SadDesa.objects.all().order_by("id")
    serializer_class = SadDesaSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get_queryset(self):
        kecamatan = self.request.query_params.get("kecamatan")
        if kecamatan:
            return SadDesa.objects.filter(kecamatan_id=kecamatan).all()
        return SadDesa.objects.all()

    @action(detail=False, permission_classes=[permissions.AllowAny])
    def me(self, request):
        desa = SadDesa.objects.get(pk=settings.DESA_ID)
        data = SadDesaSerializer(desa)
        return Response(data.data)


class SadDusunViewSet(CustomView):
    queryset = SadDusun.objects.all().order_by("id")
    serializer_class = SadDusunSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ["nama"]

    def get_queryset(self):
        desa = self.request.query_params.get("desa")
        if desa:
            return SadDusun.objects.filter(desa_id=desa).all()
        return SadDusun.objects.all()


class SadDukuhViewSet(CustomView):
    queryset = SadDukuh.objects.all().order_by("id")
    serializer_class = SadDukuhSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ["nama"]

    def get_queryset(self):
        dusun = self.request.query_params.get("dusun")
        if dusun:
            return SadDukuh.objects.filter(dusun_id=dusun).all()
        return SadDukuh.objects.all()


class SadRwViewSet(CustomView):
    queryset = SadRw.objects.all().order_by("id")
    serializer_class = SadRwSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ["rw"]

    def get_queryset(self):
        dukuh = self.request.query_params.get("dukuh")
        if dukuh:
            return SadRw.objects.filter(dukuh_id=dukuh).all()
        return SadRw.objects.all()


class SadRtViewSet(CustomView):
    queryset = SadRt.objects.all().order_by("id")
    serializer_class = SadRtSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ["rt"]

    def get_queryset(self):
        rw = self.request.query_params.get("rw")
        if rw:
            return SadRt.objects.filter(rw_id=rw).all()
        return SadRt.objects.all()


class SadKeluargaViewSet(DynamicModelViewSet):
    queryset = SadKeluarga.objects.all().order_by("id")
    serializer_class = SadKeluargaSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [filters.SearchFilter]
    search_fields = ["no_kk", "anggota__nama"]

    @action(detail=False, methods=["get"])
    def delete_all(self, request):
        SadKeluarga.objects.all().delete()
        return Response()

    def get_queryset(self):
        user = self.request.user

        if hasattr(user, "profile"):
            return SadKeluarga.objects.filter(id=user.profile.keluarga.id)
        return SadKeluarga.objects.all().order_by("id")

    @action(detail=False, methods=["post"])
    def upload(self, request):
        status = {
                "status": "success",
                "data_diinput": 0,
                "data_gagal": 0,
                "data_redundan": 0,
                "alamat_tidak_ditemukan": 0,
                }

        file = request.FILES["file"]
        converters = {'rw':str, 'rt':str}
        data = pandas.read_excel(file, converters=converters)
        data = data.replace({np.nan: None})

        checked_column = ["no_kk", "dusun", 'dukuh', 'rw', 'rt']

        if data[checked_column].isna().values.any():
            message = "Silahkan lengkapi data no_kk dan alamat"
            return Response({"message": message}, status=400)

        for item in data.to_dict("records"):
            data_alamat = {
                    "rt": item.pop("rt", None),
                    "rw": item.pop("rw", None),
                    "dukuh": item.pop("dukuh", None),
                    "dusun": item.pop("dusun", None),
                    }
            alamat = Alamat()
            get_alamat = alamat.set_from_excel(**data_alamat)
            if not get_alamat:
                status["alamat_tidak_ditemukan"] += 1
                continue

            param_filter = {"no_kk": item["no_kk"]}
            try:
                keluarga = create_or_reactivate(
                        SadKeluarga, param_filter, item
                        )
                alamat.save()
                keluarga.alamat = alamat
                keluarga.save()
            except IntegrityError:
                status["data_redundan"] += 1
                continue
            except Exception as e:
                print(item)
                print(e)
                status["data_gagal"] += 1
                continue
            status["data_diinput"] += 1
        if not status["data_diinput"]:
            status["status"] = "failed"
        return Response(status)

    def transform(self, data):
        return {
                "id": data["id"],
                "nik_kepala_keluarga": data["kepala_keluarga"]["nik"]
                if "nik" in data["kepala_keluarga"]
                else "",
                "nama_kepala_keluarga": data["kepala_keluarga"]["nama"]
                if "nama" in data["kepala_keluarga"]
                else "",
                "alamat_lengkap": data["alamat_lengkap"],
                "jalan_blok": data["jalan_blok"],
                "no_kk": data["no_kk"],
                "kode_pos": data["kode_pos"],
                "status_kesejahteraan": data["status_kesejahteraan"],
                "penghasilan": data["penghasilan"],
                "status_kk": data["status_kk"],
                "menguasai": data["menguasai"],
                }


    @action(detail=False, methods=["get"])
    def ekspor(self, request):
        with BytesIO() as b:
            writer = pandas.ExcelWriter(b)
            item = SadKeluarga.objects.all()
            serializer = SadKeluargaSerializer(item, many=True)
            df = pandas.DataFrame(list(map(self.transform, serializer.data)))
            df.reset_index(drop=True, inplace=True)
            df.to_excel(writer, sheet_name="Sheet1", index=0)
            writer.save()
            return HttpResponse(
                    b.getvalue(),
                    content_type=(
                        "application/vnd.openxmlformats-"
                        "officedocument.spreadsheetml.sheet"
                        ),
                    )


class SadPendudukViewSet(CustomView):
    queryset = SadPenduduk.objects.all().order_by("id")
    serializer_class = SadPendudukSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [filters.SearchFilter]
    search_fields = ["nama", "nik", "chip_ektp"]

    @action(detail=False, methods=["get"])
    def delete_all(self, request):
        SadPenduduk.objects.all().delete()
        return Response()

    def get_queryset(self):
        keluarga = self.request.query_params.get("keluarga")
        if keluarga:
            return SadPenduduk.objects.filter(keluarga_id=keluarga).all()
        return SadPenduduk.objects.all()

    @action(detail=False, methods=["post"])
    def upload(self, request):
        status = {
                "status": "success",
                "data_diinput": 0,
                "data_gagal": 0,
                "data_redundan": 0,
                "keluarga_tidak_ditemukan": 0,
                }

        file = request.FILES["file"]
        data = pandas.read_excel(file)
        if data[["nik", "keluarga", "nama", 'tgl_lahir']].isna().values.any():
            message = "Silahkan lengkapi data nik, keluarga dan nama"
            return Response({"message": message}, status=400)
        data = data.replace({np.nan: None})

        for item in data.to_dict("record"):
            item["keluarga"] = SadKeluarga.objects.filter(
                    no_kk=item["keluarga"]
                    ).first()
            if not item["keluarga"]:
                status["keluarga_tidak_ditemukan"] += 1
                continue

            format_data_penduduk(item)
            print(item.keys())
            param_filter = {"nik": item["nik"]}
            try:
                penduduk = create_or_reactivate(
                        SadPenduduk, param_filter, item
                        )
                status["data_diinput"] += 1

            except IntegrityError:
                print("Test Error")
                status["data_redundan"] += 1
                penduduk = SadPenduduk.objects.get(nik=item["nik"])
            except Exception as e:
                print(str(e))
                status["data_gagal"] += 1
                continue

            if not item.get('tgl_lahir'):
                print(item)
                raise Exception('tgl_lahir notfound')
            user = create_or_reactivate_user(
                    item["nik"], item["tgl_lahir"].replace("-", "")
                    )
            penduduk.user = user
            penduduk.user.save()
            penduduk.save()

        if not status["data_diinput"]:
            status["status"] = "failed"
        return Response(status)

    def transform(self, data):
        return {
                "id": data["id"],
                "nik": data["nik"],
                "chip_ektp": data["chip_ektp"],
                "nama": data["nama"],
                "tgl_lahir": data["tgl_lahir"],
                "tempat_lahir": data["tempat_lahir"],
                "jk": data["jk"],
                "alamat": data["alamat"],
                "agama": data["agama"],
                "pendidikan": data["pendidikan"],
                "pekerjaan": data["pekerjaan"],
                "status_kawin": data["status_kawin"],
                "status_penduduk": data["status_penduduk"],
                "kewarganegaraan": data["kewarganegaraan"],
                "anak_ke": data["anak_ke"],
                "golongan_darah": data["golongan_darah"],
                "status_dalam_keluarga": data["status_dalam_keluarga"],
                "no_paspor": data["no_paspor"],
                "suku": data["suku"],
                "potensi_diri": data["potensi_diri"],
                "no_hp": data["no_hp"],
                "nik_ayah": data["nik_ayah"],
                "nik_ibu": data["nik_ibu"],
                "nama_ayah": data["nama_ayah"],
                "nama_ibu": data["nama_ibu"],
                "tgl_exp_paspor": data["tgl_exp_paspor"],
                "akta_lahir": data["akta_lahir"],
                "akta_kawin": data["akta_kawin"],
                "tgl_kawin": data["tgl_kawin"],
                "akta_cerai": data["akta_cerai"],
                "tgl_cerai": data["tgl_cerai"],
                "kelainan_fisik": data["kelainan_fisik"],
                "cacat": data["cacat"],
                }

    @action(detail=False, methods=["get"])
    def ekspor(self, request):
        with BytesIO() as b:
            writer = pandas.ExcelWriter(b)
            item = SadPenduduk.objects.all()
            serializer = SadPendudukSerializer(item, many=True)
            df = pandas.DataFrame(list(map(self.transform, serializer.data)))
            df.reset_index(drop=True, inplace=True)
            df.to_excel(writer, sheet_name="Sheet1", index=0)
            writer.save()
            return HttpResponse(
                    b.getvalue(),
                    content_type=(
                        "application/vnd.openxmlformats-"
                        "officedocument.spreadsheetml.sheet"
                        ),
                    )


class SadSarprasViewSet(CustomView):
    queryset = SadSarpras.objects.all().order_by("id")
    serializer_class = SadSarprasSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ["nama_sarpras", "asal"]

    @action(detail=False, methods=["get"])
    def ekspor(self, request):
        extras = {
            "Nama Sarana Prasarana": "nama_sarpras",
            "Asal": "asal",
            "Tanggal": "tgl_awal",
            "Keadaan Awal": "keadaan_awal",
            "Keterangan": "keterangan",
            "Tahun": "tahun",
            "Url Foto": "foto"
        }
        data = (
            self.get_queryset()
            .extra(select=extras)
            .values(*extras.keys())
            .all()
        )

        workbook = Workbook()
        sheet = workbook.active

        headers = [i for i in extras.keys()]
        for index, value in enumerate(headers):
            sheet.cell(row=1, column=index + 1).value = value

        for i, x in enumerate(data):
            for idx, value in enumerate(x.values()):
                sheet.cell(row=i + 2, column=idx + 1).value = value

        output = BytesIO()
        workbook.save(output)
        response = HttpResponse(
            output.getvalue(),
            content_type="application/vnd.ms-excel",
        )
        response[
            "Content-Disposition"
        ] = 'attachment; filename="DataSaranaPrasarana.xlsx"'
        return response


class SadInventarisViewSet(CustomView):
    queryset = SadInventaris.objects.all().order_by("id")
    serializer_class = SadInventarisSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ["nama_inventaris", "asal"]

    @action(detail=False, methods=["get"])
    def ekspor(self, request):
        extras = {
            "Nama Inventaris": "nama_inventaris",
            "Asal": "asal",
            "Tanggal": "tgl_awal",
            "Keadaan Awal": "keadaan_awal",
            "Keterangan": "keterangan",
            "Tahun": "tahun",
            "Url Foto": "foto"
        }
        data = (
            self.get_queryset()
            .extra(select=extras)
            .values(*extras.keys())
            .all()
        )

        workbook = Workbook()
        sheet = workbook.active

        headers = [i for i in extras.keys()]
        for index, value in enumerate(headers):
            sheet.cell(row=1, column=index + 1).value = value

        for i, x in enumerate(data):
            for idx, value in enumerate(x.values()):
                sheet.cell(row=i + 2, column=idx + 1).value = value

        output = BytesIO()
        workbook.save(output)
        response = HttpResponse(
            output.getvalue(),
            content_type="application/vnd.ms-excel",
        )
        response[
            "Content-Disposition"
        ] = 'attachment; filename="DataInventaris.xlsx"'
        return response


class SadSuratViewSet(CustomView):
    queryset = SadSurat.objects.all().order_by("id")
    serializer_class = SadSuratSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class SigBidangViewSet(CustomView):
    queryset = SigBidang.objects.all().order_by("id")
    serializer_class = SigBidangSerializerFull
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = [
            "nbt",
            "pemilikwarga__nama",
            "pemilikwarga__nik",
            "pemiliknonwarga__nama",
            "dikuasai__no_kk",
            "penguasa_nonwarga",
            ]

    @action(detail=False, methods=["get"])
    def delete_all(self, request):
        SigBidang.objects.all().delete()
        return Response()

    def get_serializer_class(self):
        if self.action in ["list", "create"]:
            return SigBidangSerializerMini
        return SigBidangSerializerFull

    @action(detail=False, methods=["get"])
    def me(self, request):
        user = request.user
        payload = {"id": user.id, "username": user.username}

        if hasattr(user, "profile"):
            kepemilikan = user.profile.kepemilikanwarga_set.all()
            payload["kepemilikan"] = [
                    {
                        "bidang": i.bidang.id,
                        "gambar_atas": request.build_absolute_uri(
                            i.bidang.gambar_atas.url
                            )
                        if i.bidang.gambar_atas
                        else None,
                        "nbt": i.bidang.nbt,
                        "latitude": i.bidang.latitude,
                        "longitude": i.bidang.longitude,
                        "luas": i.bidang.luas,
                        "status_hak": i.bidang.status_hak,
                        "penggunaan_tanah": i.bidang.penggunaan_tanah,
                        "pemanfaatan_tanah": i.bidang.pemanfaatan_tanah,
                        "rtrw": i.bidang.rtrw,
                        "geometry": i.bidang.geometry,
                        "namabidang": i.namabidang,
                        }
                    for i in kepemilikan
                    ]

            penguasaan = user.profile.keluarga.menguasai
            if penguasaan:
                data = {
                        "bidang": penguasaan.id,
                        "nbt": penguasaan.nbt,
                        }
                payload["kepenguasaan"] = data
        return Response(payload)

    @action(detail=False, methods=["post"])
    def upload(self, request):
        file = request.FILES["file"]
        data = json.load(file)

        for item in data["features"]:
            print(item["properties"])
            data = {
                    "nbt": item["properties"]["NBT"][:20],
                    "longitude": item["properties"]["long"],
                    "latitude": item["properties"]["lat"],
                    "geometry": item["geometry"],
                    }
            # properties = item["properties"]
            # rt = properties["RT"]
            # rw = properties["RW"]
            # dusun = properties["topo_dusun"]
            # dukuh = properties['topo_dukuh']
            # sigrt = SigRt.objects.filter(
            #         rt=rt,
            #         rt__sig_rw__rw=rw,
            #         rt__sig_rw__sig_dukuh__nama = dukuh,
            #         rt__sig_rw__sig_dukuh__sig_dusun__nama = dusun
            #         ).first()
            # data["sig_rt"] = sigrt
            SigBidang.objects.create(**data)

        return Response()


class SigPemilikViewSet(CustomView):
    queryset = SigPemilik.objects.all().order_by("id")
    serializer_class = SigPemilikSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class SigDesaViewSet(CustomView):
    queryset = SigDesa.objects.all().order_by("id")
    serializer_class = SigDesaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=["get"])
    def delete_all(self, request):
        SigDesa.objects.all().delete()
        return Response()

    @action(detail=False, methods=["post"])
    def upload(self, request):
        file = request.FILES["file"]
        data = json.load(file)

        for item in data["features"]:
            item = {
                    "nama_desa": item["properties"]["topo_desa"],
                    "luas": item["properties"]["Luas"][:5],
                    "keliling": item["properties"]["Keliling"][:5],
                    "geometry": item["geometry"],
                    }
            SigDesa.objects.create(**item)

        return Response()


class SigKawasanHutanViewSet(CustomView):
    queryset = SigKawasanHutan.objects.all().order_by("id")
    serializer_class = SigKawasanHutanSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=["get"])
    def delete_all(self, request):
        SigKawasanHutan.objects.all().delete()
        return Response()

    @action(detail=False, methods=["post"])
    def upload(self, request):
        file = request.FILES["file"]
        data = json.load(file)

        for item in data["features"]:
            item = {
                    "fungsi": item["properties"]["FUNGSI"],
                    "luas": item["properties"]["LUAS"][:5],
                    "geometry": item["geometry"],
                    }
            SigKawasanHutan.objects.create(**item)

        return Response()


class SigPenggunaanTanahViewSet(CustomView):
    queryset = SigPenggunaanTanah.objects.all().order_by("id")
    serializer_class = SigPenggunaanTanahSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=["get"])
    def delete_all(self, request):
        SigPenggunaanTanah.objects.all().delete()
        return Response()

    @action(detail=False, methods=["post"])
    def upload(self, request):
        file = request.FILES["file"]
        data = json.load(file)

        for item in data["features"]:
            item = {
                    "dusun": item["properties"]["NAMA_DUSUN"],
                    "penggunaan": item["properties"]["Penggunaan"],
                    "luas": item["properties"]["Luas"][:5],
                    "geometry": item["geometry"],
                    }
            SigPenggunaanTanah.objects.create(**item)

        return Response()


class SigStatusTanahViewSet(CustomView):
    queryset = SigStatusTanah.objects.all().order_by("id")
    serializer_class = SigStatusTanahSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=["get"])
    def delete_all(self, request):
        SigStatusTanah.objects.all().delete()
        return Response()

    @action(detail=False, methods=["post"])
    def upload(self, request):
        file = request.FILES["file"]
        data = json.load(file)

        for item in data["features"]:
            item = {
                    "tipe": item["properties"]["TIPEHAK"],
                    "geometry": item["geometry"],
                    }
            SigStatusTanah.objects.create(**item)

        return Response()


class SigArahanViewSet(CustomView):
    queryset = SigArahan.objects.all().order_by("id")
    serializer_class = SigArahanSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=["get"])
    def delete_all(self, request):
        SigArahan.objects.all().delete()
        return Response()

    @action(detail=False, methods=["post"])
    def upload(self, request):
        file = request.FILES["file"]
        data = json.load(file)

        for item in data["features"]:
            item = {
                    "luas": item["properties"]["LUAS"][:4],
                    "arahan": item["properties"]["ARAHAN_RUA"],
                    "pola_ruang": item["properties"]["POLA_RUANG"],
                    "fungsi": item["properties"]["FUNGSI"],
                    "geometry": item["geometry"],
                    }
            SigArahan.objects.create(**item)

        return Response()


class SigDusunViewSet(CustomView):
    queryset = SigDusun.objects.all().order_by("id")
    serializer_class = SigDusunSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=["get"])
    def delete_all(self, request):
        SigDusun.objects.all().delete()
        return Response()

    @action(detail=False, methods=["post"])
    def upload(self, request):
        file = request.FILES["file"]
        data = json.load(file)

        for item in data["features"]:
            desa = SigDesa.objects.get(
                    nama_desa=item["properties"]["topo_desa"]
                    )
            item = {
                    "sig_desa": desa,
                    "nama_dusun": item["properties"]["topo_dusun"],
                    "luas": item["properties"]["Luas"][:5],
                    "keliling": item["properties"]["Keliling"][:5],
                    "geometry": item["geometry"],
                    }
            SigDusun.objects.create(**item)
        return Response()


class SigDukuhViewSet(CustomView):
    queryset = SigDukuh.objects.all().order_by("id")
    serializer_class = SigDukuhSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=["get"])
    def delete_all(self, request):
        SigDukuh.objects.all().delete()
        return Response()

    @action(detail=False, methods=["post"])
    def upload(self, request):
        file = request.FILES["file"]
        data = json.load(file)

        for item in data["features"]:
            dusun = SigDusun.objects.get(
                    nama_dusun=item["properties"]["topo_dusun"]
                    )
            item = {
                    "sig_dusun": dusun,
                    "nama_dukuh": item["properties"]["topo_dukuh"],
                    "luas": item["properties"]["Luas"][:5],
                    "keliling": item["properties"]["Keliling"][:5],
                    "geometry": item["geometry"],
                    }
            SigDukuh.objects.create(**item)
        return Response()


class SigRwViewSet(CustomView):
    queryset = SigRw.objects.all().order_by("id")
    serializer_class = SigRwSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=["get"])
    def delete_all(self, request):
        SigRw.objects.all().delete()
        return Response()

    @action(detail=False, methods=["post"])
    def upload(self, request):
        file = request.FILES["file"]
        data = json.load(file)

        for item in data["features"]:
            dusun = SigDusun.objects.get(
                    nama_dukuh=item["properties"]["topo_dusun"]
                    )
            item = {
                    "sig_dukuh": dukuh,
                    "rw": item["properties"]["RW"],
                    "geometry": item["geometry"],
                    }
            SigRw.objects.create(**item)
        return Response()


class SigRtViewSet(CustomView):
    queryset = SigRt.objects.all().order_by("id")
    serializer_class = SigRtSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=["get"])
    def delete_all(self, request):
        SigRt.objects.all().delete()
        return Response()

    @action(detail=False, methods=["post"])
    def upload(self, request):
        file = request.FILES["file"]
        data = json.load(file)

        for item in data["features"]:
            rw = SigRw.objects.get(rw=item["properties"]["RW"])
            item = {
                    "sig_rw": rw,
                    "rt": item["properties"]["RT"],
                    "geometry": item["geometry"],
                    }
            SigRt.objects.create(**item)
        return Response()


class KategoriArtikelViewSet(DynamicModelViewSet):
    queryset = KategoriArtikel.objects.all().order_by("id")
    serializer_class = KategoriArtikelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ["nama"]


class ArtikelViewSet(DynamicModelViewSet):
    queryset = Artikel.objects.all().order_by("-id")
    serializer_class = ArtikelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ["judul"]


class SliderViewSet(DynamicModelViewSet):
    queryset = Slider.objects.all().order_by("id")
    serializer_class = SliderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class KategoriLaporViewSet(DynamicModelViewSet):
    queryset = KategoriLapor.objects.all().order_by("id")
    serializer_class = KategoriLaporSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [filters.SearchFilter]
    search_fields = ["nama"]


class StatusLaporViewSet(DynamicModelViewSet):
    queryset = StatusLapor.objects.all().order_by("id")
    serializer_class = StatusLaporSerializer
    permission_classes = [permissions.IsAuthenticated]


class LaporViewSet(CustomView):
    queryset = Lapor.objects.all().order_by("-id")
    serializer_class = LaporSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ["judul"]


class KategoriInformasiViewSet(DynamicModelViewSet):
    queryset = KategoriInformasi.objects.all().order_by("id")
    serializer_class = KategoriInformasiSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ["nama"]


class InformasiViewSet(DynamicModelViewSet):
    queryset = Informasi.objects.all().order_by("id")
    serializer_class = InformasiSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ["judul"]


class KategoriPotensiViewSet(DynamicModelViewSet):
    queryset = KategoriPotensi.objects.all().order_by("id")
    serializer_class = KategoriPotensiSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class PotensiViewSet(DynamicModelViewSet):
    queryset = Potensi.objects.all().order_by("-id")
    serializer_class = PotensiSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        kategori = self.request.query_params.get("kategori")
        if kategori:
            return (
                    Potensi.objects.filter(kategori=kategori).all().order_by("-id")
                    )
            return Potensi.objects.all().order_by("-id")


class KategoriPendapatanViewSet(DynamicModelViewSet):
    queryset = KategoriPendapatan.objects.all().order_by("id")
    serializer_class = KategoriPendapatanSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



class KategoriBelanjaViewSet(DynamicModelViewSet):
    queryset = KategoriBelanja.objects.all().order_by("id")
    serializer_class = KategoriBelanjaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class KategoriTahunViewSet(DynamicModelViewSet):
    queryset = KategoriTahun.objects.all().order_by("id")
    serializer_class = KategoriTahunSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PendapatanViewSet(DynamicModelViewSet):
    queryset = Pendapatan.objects.all().order_by("id")
    serializer_class = PendapatanSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        tahun = self.request.query_params.get("tahun")
        if tahun:
            return (
                    Pendapatan.objects.all()
                    .filter(tahun_id=tahun)
                    .order_by("nama")
                    )
            return Pendapatan.objects.all()


class BelanjaViewSet(DynamicModelViewSet):
    queryset = Belanja.objects.all().order_by("id")
    serializer_class = BelanjaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        tahun = self.request.query_params.get("tahun")
        if tahun:
            return (
                    Belanja.objects.all().filter(tahun_id=tahun).order_by("nama")
                    )
            return Belanja.objects.all()


class SuratMasukViewSet(DynamicModelViewSet):
    queryset = SuratMasuk.objects.all().order_by("id")
    serializer_class = SuratMasukSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [filters.SearchFilter]
    search_fields = ["perihal", "keterangan"]

    @action(detail=False, methods=["get"])
    def ekspor(self, request):
        extras = {
            "No Surat": "no_surat",
            "Tanggal Terima": "tgl_terima",
            "Tanggal Surat": "tgl_surat",
            "Pengirim": "pengirim",
            "Kepada": "kepada",
            "Perihal": "perihal",
            "Keterangan": "keterangan",
            "Url Surat": "arsip_suratmasuk"
        }
        data = (
            self.get_queryset()
            .extra(select=extras)
            .values(*extras.keys())
            .all()
        )

        workbook = Workbook()
        sheet = workbook.active

        headers = [i for i in extras.keys()]
        for index, value in enumerate(headers):
            sheet.cell(row=1, column=index + 1).value = value

        for i, x in enumerate(data):
            for idx, value in enumerate(x.values()):
                sheet.cell(row=i + 2, column=idx + 1).value = value

        output = BytesIO()
        workbook.save(output)
        response = HttpResponse(
            output.getvalue(),
            content_type="application/vnd.ms-excel",
        )
        response[
            "Content-Disposition"
        ] = 'attachment; filename="ArsipSuratMasuk.xlsx"'
        return response


class SuratKeluarViewSet(DynamicModelViewSet):
    queryset = SuratKeluar.objects.all().order_by("id")
    serializer_class = SuratKeluarSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [filters.SearchFilter]
    search_fields = ["perihal", "keterangan"]

    @action(detail=False, methods=["get"])
    def ekspor(self, request):
        extras = {
            "No Surat": "no_surat",
            "Tanggal Kirim": "tgl_kirim",
            "Tanggal Surat": "tgl_surat",
            "Pengirim": "pengirim",
            "Kepada": "kepada",
            "Perihal": "perihal",
            "Keterangan": "keterangan",
            "Url Surat": "arsip_suratkeluar"
        }
        data = (
            self.get_queryset()
            .extra(select=extras)
            .values(*extras.keys())
            .all()
        )

        workbook = Workbook()
        sheet = workbook.active

        headers = [i for i in extras.keys()]
        for index, value in enumerate(headers):
            sheet.cell(row=1, column=index + 1).value = value

        for i, x in enumerate(data):
            for idx, value in enumerate(x.values()):
                sheet.cell(row=i + 2, column=idx + 1).value = value

        output = BytesIO()
        workbook.save(output)
        response = HttpResponse(
            output.getvalue(),
            content_type="application/vnd.ms-excel",
        )
        response[
            "Content-Disposition"
        ] = 'attachment; filename="ArsipSuratKeluar.xlsx"'
        return response


class PekerjaanViewSet(DynamicModelViewSet):
    queryset = Pekerjaan.objects.all().order_by("id")
    serializer_class = PekerjaanSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [filters.SearchFilter]
    search_fields = ["nama"]


class PendidikanViewSet(DynamicModelViewSet):
    queryset = Pendidikan.objects.all().order_by("id")
    serializer_class = PendidikanSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [filters.SearchFilter]
    search_fields = ["nama"]


class AgamaViewSet(DynamicModelViewSet):
    queryset = Agama.objects.all().order_by("id")
    serializer_class = AgamaSerializer
    permission_classes = [permissions.IsAuthenticated]


class KelainanFisikViewSet(DynamicModelViewSet):
    queryset = KelainanFisik.objects.all().order_by("id")
    serializer_class = KelainanFisikSerializer
    permission_classes = [permissions.IsAuthenticated]


class CacatViewSet(DynamicModelViewSet):
    queryset = Cacat.objects.all().order_by("id")
    serializer_class = CacatSerializer
    permission_classes = [permissions.IsAuthenticated]


class StatusPerkawinanViewSet(DynamicModelViewSet):
    queryset = StatusPerkawinan.objects.all().order_by("id")
    serializer_class = StatusPerkawinanSerializer
    permission_classes = [permissions.IsAuthenticated]


class KewarganegaraanViewSet(DynamicModelViewSet):
    queryset = Kewarganegaraan.objects.all().order_by("id")
    serializer_class = KewarganegaraanSerializer
    permission_classes = [permissions.IsAuthenticated]


class GoldarViewSet(DynamicModelViewSet):
    queryset = Goldar.objects.all().order_by("id")
    serializer_class = GoldarSerializer
    permission_classes = [permissions.IsAuthenticated]


class StatusDlmKeluargaViewSet(DynamicModelViewSet):
    queryset = StatusDlmKeluarga.objects.all().order_by("id")
    serializer_class = StatusDlmKeluargaSerializer
    permission_classes = [permissions.IsAuthenticated]


class StatusKesejahteraanViewSet(DynamicModelViewSet):
    queryset = StatusKesejahteraan.objects.all().order_by("id")
    serializer_class = StatusKesejahteraanSerializer
    permission_classes = [permissions.IsAuthenticated]


class StatusWargaViewSet(DynamicModelViewSet):
    queryset = StatusWarga.objects.all().order_by("id")
    serializer_class = StatusWargaSerializer
    permission_classes = [permissions.IsAuthenticated]


class StatusDatangMasukViewSet(DynamicModelViewSet):
    queryset = StatusDatangMasuk.objects.all().order_by("id")
    serializer_class = StatusDatangMasukSerializer
    permission_classes = [permissions.IsAuthenticated]


class AsalViewSet(DynamicModelViewSet):
    queryset = Asal.objects.all().order_by("id")
    serializer_class = AsalSerializer
    permission_classes = [permissions.IsAuthenticated]


class KeadaanAwalViewSet(DynamicModelViewSet):
    queryset = KeadaanAwal.objects.all().order_by("id")
    serializer_class = KeadaanAwalSerializer
    permission_classes = [permissions.IsAuthenticated]


class JabatanViewSet(DynamicModelViewSet):
    queryset = Jabatan.objects.all().order_by("id")
    serializer_class = JabatanSerializer
    permission_classes = [permissions.IsAuthenticated]


class StatusPnsViewSet(DynamicModelViewSet):
    queryset = StatusPns.objects.all().order_by("id")
    serializer_class = StatusPnsSerializer
    permission_classes = [permissions.IsAuthenticated]


class GolonganViewSet(DynamicModelViewSet):
    queryset = Golongan.objects.all().order_by("id")
    serializer_class = GolonganSerializer
    permission_classes = [permissions.IsAuthenticated]


class JenisKelahiranViewSet(DynamicModelViewSet):
    queryset = JenisKelahiran.objects.all().order_by("id")
    serializer_class = JenisKelahiranSerializer
    permission_classes = [permissions.IsAuthenticated]


class JenisTempatViewSet(DynamicModelViewSet):
    queryset = JenisTempat.objects.all().order_by("id")
    serializer_class = JenisTempatSerializer
    permission_classes = [permissions.IsAuthenticated]


class TenagaKesehatanViewSet(DynamicModelViewSet):
    queryset = TenagaKesehatan.objects.all().order_by("id")
    serializer_class = TenagaKesehatanSerializer
    permission_classes = [permissions.IsAuthenticated]


class AbsensiViewSet(DynamicModelViewSet):
    queryset = Absensi.objects.all().order_by("-id")
    serializer_class = AbsensiSerializer
    permission_classes = [AllowAny]


class AlasanIzinViewSet(DynamicModelViewSet):
    queryset = AlasanIzin.objects.all().order_by("id")
    serializer_class = AlasanIzinSerializer
    permission_classes = [permissions.IsAuthenticated]


def string_to_date(text):
    return datetime.strptime(text, "%Y-%m-%d").astimezone(
            pytz.timezone(settings.TIME_ZONE)
            )


class LaporanAbsensiViewSet(DynamicModelViewSet):
    queryset = Absensi.objects.order_by("id").all()
    serializer_class = AbsensiSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get_serializer_class(self):
        print(self.action)
        if self.action not in ["list", "create"]:
            raise NotFound("Operasi ini tidak tersedia")
        return self.serializer_class

    def get_queryset(self):
        start = self.request.query_params.get("start")
        end = self.request.query_params.get("end")
        pegawai_id = self.request.query_params.get("pegawai_id")
        if not start or not end:
            raise APIException(
                    "Need start date and end date for filtering", 400
                    )
            start_date = string_to_date(start)
        end_date = string_to_date(end)

        queryset = Absensi.objects.filter(
                pegawai_id=pegawai_id,
                jam_masuk__gte=start_date,
                jam_masuk__lte=end_date,
                )

        return queryset.order_by("id").all()


class DemografiViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        type_param = request.query_params.get("type")
        data = []
        query_s = {
                "pekerjaan": SadPenduduk.objects.all()
                .annotate(name=F("pekerjaan"))
                .values("name")
                .annotate(y=Count("pekerjaan"))
                .all(),
                "jk": SadPenduduk.objects.all()
                .annotate(name=F("jk"))
                .values("name")
                .annotate(y=Count("jk"))
                .all(),
                "agama": SadPenduduk.objects.all()
                .annotate(name=F("agama"))
                .values("name")
                .annotate(y=Count("agama"))
                .all(),
                "pendidikan": SadPenduduk.objects.all()
                .annotate(name=F("pendidikan"))
                .values("name")
                .annotate(y=Count("pendidikan")),
                "potensi_diri": SadPenduduk.objects.all()
                .annotate(name=F("potensi_diri"))
                .values("name")
                .annotate(y=Count("potensi_diri")),
                "kepadatan": SadPenduduk.objects.annotate(
                    name=F("keluarga__alamat__dusun__nama")
                    )
                .values("name")
                .annotate(y=Count("keluarga__alamat__dusun")),
                "mbr": SadKeluarga.objects.all()
                .annotate(name=F("status_kesejahteraan"))
                .values("name")
                .annotate(y=Count("status_kesejahteraan")),
                "penghasilan": SadPenduduk.objects.annotate(
                    name=F("keluarga__alamat__dusun__nama")
                    )
                .values("name")
                .annotate(y=Avg("keluarga__penghasilan")),
                }
        if type_param:
            data = list(query_s[type_param].all())
        return Response({"data": data})


class DashboardViewSet(viewsets.ViewSet):
    serializer_class = DashboardSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get(self, request):
        dusun = SadDusun.objects.all().aggregate(count=Count("id"))
        penduduk = SadPenduduk.objects.all().aggregate(count=Count("id"))
        keluarga = SadKeluarga.objects.all().aggregate(count=Count("id"))

        keluarga = SadKeluarga.objects.raw(
                """
           SELECT alamat.dusun_id as id, sad_dusun.nama as nama,
                   count (*) as k
           FROM sad_keluarga t1
           INNER JOIN alamat ON t1.alamat_id=alamat.id
           inner join sad_dusun on alamat.dusun_id=sad_dusun.id
           group by alamat.dusun_id, sad_dusun.nama"""
           )

        penduduk = SadPenduduk.objects.raw(
                """
            SELECT alamat.dusun_id as id, sad_dusun.nama as nama, count (*) as p FROM sad_penduduk
            inner join sad_keluarga on sad_penduduk.keluarga_id=sad_keluarga.no_kk
            inner join alamat ON sad_keluarga.alamat_id=alamat.id
            inner join sad_dusun on alamat.dusun_id=sad_dusun.id
            group by alamat.dusun_id, sad_dusun.nama"""
            )

        results = [
                {
                    "name": x.nama,
                    "id": x.id,
                    "penduduk": x.p,
                    "keluarga": list(
                        filter(lambda item, x=x: item.id == x.id, keluarga)
                        )[0].k,
                    }
                for i, x in enumerate(penduduk)
                ]
        return Response({"data": results})


class CctvViewSet(DynamicModelViewSet):
    queryset = Cctv.objects.all().order_by("-id")
    serializer_class = CctvSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    @action(detail=False, methods=["get"])
    def delete_all(self, request):
        Cctv.objects.all().delete()
        return Response()

    @action(detail=False, methods=["post"])
    def upload(self, request):
        file = request.FILES["file"]
        data = json.load(file)

        for item in data["features"]:
            item = {
                    "nama": item["properties"]["nama"],
                    "link": item["properties"]["link"],
                    "koordinat": item["geometry"],
                    }
            Cctv.objects.create(**item)

        return Response()


class BiayaKunjunganViewSet(DynamicModelViewSet):
    queryset = BiayaKunjungan.objects.all().order_by("id")
    serializer_class = BiayaKunjunganSerializer
    permission_classes = [permissions.IsAuthenticated]


class KunjunganViewSet(DynamicModelViewSet):
    queryset = Kunjungan.objects.all().order_by("id")
    serializer_class = KunjunganSerializer
    permission_classes = [permissions.IsAuthenticated]