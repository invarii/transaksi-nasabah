import jinja2
import pdfkit

from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User, Group


def render_mail(mail_type, data):
    template_folder = str(settings.BASE_DIR) + "/mail_templates"
    template_loader = jinja2.FileSystemLoader(template_folder)
    template_env = jinja2.Environment(loader=template_loader)
    template_name = mail_type + ".html"
    logo_path = template_folder + "/logo.png"
    template = template_env.get_template(template_name)
    output = template.render(
        surat=data, logo=logo_path, tanggal=timezone.now().strftime("%d %B %Y")
    )

    pdf = pdfkit.from_string(output, False)
    return pdf


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
