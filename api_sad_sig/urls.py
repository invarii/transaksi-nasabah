from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

import v1.urls as v1_urls

router = routers.DefaultRouter()
router.registry.extend(v1_urls.router.registry)

url_collections = []

urlpatterns = [
    path("admin/", admin.site.urls),
    path("v1/", include(router.urls + url_collections)),
    path("swagger/", include("rest_framework.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
