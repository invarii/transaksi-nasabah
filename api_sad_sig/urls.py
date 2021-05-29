"""api_sad_sig URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

import v1.urls as v1_urls
import users.urls as users_urls
import layananperistiwa.urls as layanan_urls
from layananperistiwa.views import list_layanan_surat

router = routers.DefaultRouter()
router.registry.extend(users_urls.router.registry)
router.registry.extend(v1_urls.router.registry)
router.registry.extend(layanan_urls.router.registry)

url_collections = []
url_collections.extend(users_urls.urlpatterns)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("v1/", include(router.urls + url_collections)),
    path("swagger/", include("rest_framework.urls")),
    path("v1/daftarlayanansurat", list_layanan_surat),
    path("v1/dashboard", v1_urls.DashboardViewSet.as_view({"get": "get"})),
    path("v1/demografi", v1_urls.DemografiViewSet.as_view({"get": "get"})),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
