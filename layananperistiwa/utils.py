import jinja2
import pdfkit
from datetime import datetime

from django.conf import settings
from django.utils import timezone
from v1.models import SadDesa


def thousand_delimiter(val):
    return "{0:,}".format(val).replace(",", ".")


def render_new_mail(mail_type, data):
    media_root = settings.MEDIA_ROOT
    template_folder = str(settings.BASE_DIR) + "/mail_templates"
    template_loader = jinja2.FileSystemLoader(template_folder)
    template_env = jinja2.Environment(loader=template_loader)
    template_name = mail_type + ".html"
    logo_path = template_folder + "/logo.png"
    template = template_env.get_template(template_name)
    desa = SadDesa.objects.get(pk=settings.DESA_ID)
    output = template.render(
        media_root=media_root,
        desa=desa,
        surat=data,
        logo=logo_path,
        tanggal=timezone.now().strftime("%d %B %Y"),
        datetime=datetime,
        thousand_delimiter=thousand_delimiter,
    )

    options = {"page-size": "A4"}
    pdf = pdfkit.from_string(output, False, options=options)
    return pdf


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
