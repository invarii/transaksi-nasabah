from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from v1.models import Artikel, Slider, Potensi, Lapor


def delete_image(sender, instance, **kwargs):
    instance.gambar.delete(save=False)


receiver(pre_delete, sender=Artikel)(delete_image)
receiver(pre_delete, sender=Slider)(delete_image)
receiver(pre_delete, sender=Potensi)(delete_image)
receiver(pre_delete, sender=Lapor)(delete_image)
