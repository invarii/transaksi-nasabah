import os

from rest_framework import status
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from dynamic_rest.serializers import DynamicModelSerializer
from dynamic_rest.viewsets import DynamicModelViewSet

# Excluded column in serializer
util_columns = [
    "created_by",
    "updated_by",
    "deleted_by",
    "created_at",
    "updated_at",
    "deleted_at",
]


def file_destination(instance, filename):
    extension = os.path.splitext(filename)[1]
    new_filename = timezone.now().strftime("%Y%m%d%H%M%S")
    folder_name = instance.__class__.__name__.lower()
    return f"{folder_name}/{new_filename}{extension}"


class CustomView(DynamicModelViewSet):
    def destroy(self, request, pk, format=None):
        data = self.get_object()
        data.deleted_by = request.user
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


class CustomSerializer(DynamicModelSerializer):
    extra_kwargs = {"created_by": {"write_only": True}}

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        user = self.context["request"].user
        validated_data["updated_by"] = user
        data = super().update(instance, validated_data)
        data.save()
        return data

    class Meta:
        model = None


def create_or_reactivate(model, filter_param, data):
    instance = model.all_objects.filter(**filter_param).dead().first()

    if instance:
        instance.deleted_by = None
        instance.deleted_at = None
        instance.save()

        model.objects.filter(pk=instance.pk).update(**data)
        instance.refresh_from_db()
    else:
        instance = model.objects.create(**data)
    instance.save()
    return instance


def create_or_reactivate_user(username, password):
    user = User.objects.filter(username=username).first()
    group = Group.objects.get(name="penduduk")

    if not user:
        user = User.objects.create(username=username)
        user.set_password(password)
        user.groups.add(group)
        user.save()
    elif not user.is_active:
        user.is_active = True
        user.set_password(password)
        user.save()
    return user
