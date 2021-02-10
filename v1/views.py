from rest_framework import permissions
from django.conf import settings
from django.db.utils import IntegrityError
from django.http import HttpResponse
from dynamic_rest.viewsets import DynamicModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters, viewsets
from rest_framework.exceptions import NotFound, APIException
from django.db.models import Count
import pytz
from datetime import datetime


import pandas
import json
from io import BytesIO
import numpy as np

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

    filter_backends = [filters.SearchFilter]
    search_fields = ["id", "nama_kab_kota"]

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

    filter_backends = [filters.SearchFilter]
    search_fields = ["id", "nama_kecamatan"]

    def get_queryset(self):
        kabkota = self.request.query_params.get("kabkota")
        if kabkota:
            return SadKecamatan.objects.filter(kab_kota_id=kabkota).all()
        return SadKecamatan.objects.all()


class SadDesaViewSet(CustomView):
    queryset = SadDesa.objects.all().order_by("id")
    serializer_class = SadDesaSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ["id", "nama_desa"]

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


class SadRwViewSet(CustomView):
    queryset = SadRw.objects.all().order_by("id")
    serializer_class = SadRwSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ["rw"]

    def get_queryset(self):
        dusun = self.request.query_params.get("dusun")
        if dusun:
            return SadRw.objects.filter(dusun=dusun).all()
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
    search_fields = ["no_kk"]

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
        data = pandas.read_excel(file)
        data = data.replace({np.nan: None})

        checked_column = ["no_kk", "dusun"]
        if "rt" in data.columns:
            checked_column.extend(["rw", "rt"])

        if data[checked_column].isna().values.any():
            message = "Silahkan lengkapi data no_kk dan alamat"
            return Response({"message": message}, status=400)

        for item in data.to_dict("records"):
            data_alamat = {
                "rt": item.pop("rt", None),
                "rw": item.pop("rw", None),
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

    @action(detail=False, methods=["get"])
    def ekspor(self, request):
        with BytesIO() as b:
            writer = pandas.ExcelWriter(b)
            item = SadKeluarga.objects.all()
            serializer = SadKeluargaSerializer(item, many=True)
            df = pandas.DataFrame(serializer.data)
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
        if data[["nik", "keluarga", "nama"]].isna().values.any():
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

            user = create_or_reactivate_user(
                item["nik"], item["tgl_lahir"].replace("-", "")
            )
            penduduk.user = user
            penduduk.user.save()
            penduduk.save()

        if not status["data_diinput"]:
            status["status"] = "failed"
        return Response(status)

    @action(detail=False, methods=["get"])
    def ekspor(self, request):
        with BytesIO() as b:
            writer = pandas.ExcelWriter(b)
            item = SadPenduduk.objects.all()
            serializer = SadPendudukSerializer(item, many=True)
            df = pandas.DataFrame(serializer.data)
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


class SadInventarisViewSet(CustomView):
    queryset = SadInventaris.objects.all().order_by("id")
    serializer_class = SadInventarisSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ["nama_inventaris", "asal"]


class SadSuratViewSet(CustomView):
    queryset = SadSurat.objects.all().order_by("id")
    serializer_class = SadSuratSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class SigBidangViewSet(CustomView):
    queryset = SigBidang.objects.all().order_by("id")
    serializer_class = SigBidangSerializerFull
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ["nbt", "pemilikwarga__nama", "pemiliknonwarga__nama"]

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
                    "gambar_atas": request.build_absolute_uri(i.bidang.gambar_atas.url) if i.bidang.gambar_atas else None,
                    "nbt": i.bidang.nbt,
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
                "geometry": item["geometry"],
            }
            properties = item["properties"]
            if properties.get("RT"):
                rt = properties["RT"]
                rw = properties["RW"]
                dusun = properties["topo_dusun"]
                sigrt = SigRt.objects.filter(
                    rt=rt, sig_rw__rw=rw, sig_rw__sigdusun__nama_dusun=dusun
                ).first()
                data["sig_rt"] = sigrt
            elif properties.get("topo_dusun"):
                dusun = properties["topo_dusun"]
                sigdusun = SigDusun.objects.filter(nama_dusun=dusun).first()
                data["sig_dusun"] = sigdusun
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
                "luas": item["properties"]["Luas"],
                "keliling": item["properties"]["Keliling"],
                "geometry": item["geometry"],
            }
            SigDesa.objects.create(**item)

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
                "luas": item["properties"]["Luas"],
                "keliling": item["properties"]["Keliling"],
                "geometry": item["geometry"],
            }
            SigDusun.objects.create(**item)
        return Response()


class SigDukuhViewSet(CustomView):
    queryset = SigDukuh.objects.all().order_by("id")
    serializer_class = SigDukuhSerializer
    permission_classes = [permissions.IsAuthenticated]

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
                "luas": item["properties"]["Luas"],
                "keliling": item["properties"]["Keliling"],
                "geometry": item["geometry"],
            }
            SigDukuh.objects.create(**item)
        return Response()


class SigDukuh2ViewSet(CustomView):
    queryset = SigDukuh2.objects.all().order_by("id")
    serializer_class = SigDukuh2Serializer
    permission_classes = [IsAdminUserOrReadOnly]

    @action(detail=False, methods=["get"])
    def delete_all(self, request):
        SigDukuh2.objects.all().delete()
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
                "nama_dukuh": item["properties"]["topo_dukuh"],
                "luas": item["properties"]["Luas"],
                "keliling": item["properties"]["Keliling"],
                "geometry": item["geometry"],
            }
            SigDukuh2.objects.create(**item)
        return Response()


class SigRwViewSet(CustomView):
    queryset = SigRw.objects.all().order_by("id")
    serializer_class = SigRwSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"])
    def delete_all(self, request):
        SigRw.objects.all().delete()
        return Response()

    @action(detail=False, methods=["post"])
    def upload(self, request):
        file = request.FILES["file"]
        data = json.load(file)

        for item in data["features"]:
            dukuh = SigDukuh.objects.get(
                nama_dukuh=item["properties"]["topo_dukuh"]
            )
            item = {
                "sig_dukuh": dukuh,
                "rw": item["properties"]["RW"],
                "geometry": item["geometry"],
            }
            SigRw.objects.create(**item)
        return Response()


class SigRw2ViewSet(CustomView):
    queryset = SigRw2.objects.all().order_by("id")
    serializer_class = SigRw2Serializer
    permission_classes = [IsAdminUserOrReadOnly]

    @action(detail=False, methods=["get"])
    def delete_all(self, request):
        SigRw2.objects.all().delete()
        return Response()

    @action(detail=False, methods=["post"])
    def upload(self, request):
        file = request.FILES["file"]
        data = json.load(file)

        for item in data["features"]:
            dukuh2 = SigDukuh2.objects.get(
                nama_dukuh=item["properties"]["topo_dukuh"]
            )
            item = {
                "sig_dukuh2": dukuh2,
                "rw": item["properties"]["RW"],
                "geometry": item["geometry"],
            }
            SigRw2.objects.create(**item)
        return Response()


class SigRtViewSet(CustomView):
    queryset = SigRt.objects.all().order_by("id")
    serializer_class = SigRtSerializer
    permission_classes = [permissions.IsAuthenticated]

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


class SigRt2ViewSet(CustomView):
    queryset = SigRt2.objects.all().order_by("id")
    serializer_class = SigRt2Serializer
    permission_classes = [IsAdminUserOrReadOnly]

    @action(detail=False, methods=["get"])
    def delete_all(self, request):
        SigRt2.objects.all().delete()
        return Response()

    @action(detail=False, methods=["post"])
    def upload(self, request):
        file = request.FILES["file"]
        data = json.load(file)

        for item in data["features"]:
            rw2 = SigRw2.objects.get(rw=item["properties"]["RW"])
            item = {
                "sig_rw2": rw2,
                "rt": item["properties"]["RT"],
                "geometry": item["geometry"],
            }
            SigRt2.objects.create(**item)
        return Response()


class KategoriArtikelViewSet(DynamicModelViewSet):
    queryset = KategoriArtikel.objects.all().order_by("id")
    serializer_class = KategoriArtikelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ["nama"]


class ArtikelViewSet(DynamicModelViewSet):
    queryset = Artikel.objects.all().order_by("id")
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

    filter_backends = [filters.SearchFilter]
    search_fields = ["nama"]


class PotensiViewSet(DynamicModelViewSet):
    queryset = Potensi.objects.all().order_by("-id")
    serializer_class = PotensiSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ["judul"]

    def get_queryset(self):
        kategori = self.request.query_params.get("kategori")
        if kategori:
            return Potensi.objects.filter(kategori=kategori).all().order_by("-id")
        return Potensi.objects.all().order_by("-id")


class KategoriPendapatanViewSet(DynamicModelViewSet):
    queryset = KategoriPendapatan.objects.all().order_by("id")
    serializer_class = KategoriPendapatanSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ["nama"]


class KategoriBelanjaViewSet(DynamicModelViewSet):
    queryset = KategoriBelanja.objects.all().order_by("id")
    serializer_class = KategoriBelanjaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ["nama"]


class KategoriTahunViewSet(DynamicModelViewSet):
    queryset = KategoriTahun.objects.all().order_by("id")
    serializer_class = KategoriTahunSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PendapatanViewSet(DynamicModelViewSet):
    queryset = Pendapatan.objects.all().order_by("id")
    serializer_class = PendapatanSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ["nama"]

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

    filter_backends = [filters.SearchFilter]
    search_fields = ["nama"]

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


class SuratKeluarViewSet(DynamicModelViewSet):
    queryset = SuratKeluar.objects.all().order_by("id")
    serializer_class = SuratKeluarSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [filters.SearchFilter]
    search_fields = ["perihal", "keterangan"]


class PekerjaanViewSet(DynamicModelViewSet):
    queryset = Pekerjaan.objects.all().order_by("id")
    serializer_class = PekerjaanSerializer
    permission_classes = [permissions.IsAuthenticated]


class PendidikanViewSet(DynamicModelViewSet):
    queryset = Pendidikan.objects.all().order_by("id")
    serializer_class = PendidikanSerializer
    permission_classes = [permissions.IsAuthenticated]


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
    permission_classes = [IsAdminUserOrReadOnly]


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

class DashboardViewSet(viewsets.ViewSet):
    serializer_class = DashboardSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get(self, request):
        dusun = SadDusun.objects.all().aggregate(count=Count("id"))
        penduduk = SadPenduduk.objects.all().aggregate(count=Count("id"))
        keluarga = SadKeluarga.objects.all().aggregate(count=Count("id"))
        
        # dashboard = Dashboard(dusun=dusun['count'], penduduk=penduduk['count'], keluarga=keluarga["count"]) 
        # results = DashboardSerializer(dashboard).data

        # return Response({
        #     "data": results

        keluarga = SadKeluarga.objects.raw('''
            SELECT alamat.dusun_id as id, sad_dusun.nama as nama, count (*) as k FROM sad_keluarga t1 
            INNER JOIN alamat ON t1.alamat_id=alamat.id 
            inner join sad_dusun on alamat.dusun_id=sad_dusun.id
            group by alamat.dusun_id, sad_dusun.nama''')
        
        item =[]
        for p in keluarga:
            item.append({'dusun_id':p.id, 'nama_dusun':p.nama, "totalkeluarga":p.k})
        
        return Response({
            "data": item
        })

class CctvViewSet(DynamicModelViewSet):
    queryset = Cctv.objects.all().order_by("-id")
    serializer_class = CctvSerializer
    permission_classes = [IsAdminUserOrReadOnly]
