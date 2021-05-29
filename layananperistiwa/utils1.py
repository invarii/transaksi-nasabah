import locale
import jinja2
import pdfkit

from django.conf import settings
from django.utils import timezone
from v1.models import SadDesa


def render_mail(mail_type, data):
    locale.setlocale(locale.LC_TIME, "id_ID.UTF-8")
    template_folder = str(settings.BASE_DIR) + "/mail_templates"
    template_loader = jinja2.FileSystemLoader(template_folder)
    template_env = jinja2.Environment(loader=template_loader)
    template_name = mail_type + ".html"
    logo_path = template_folder + "/logo.png"
    template = template_env.get_template(template_name)
    desa = SadDesa.objects.get(pk=settings.DESA_ID)
    output = template.render(
        desa=desa, surat=data, logo=logo_path, tanggal=timezone.now().strftime("%d %B %Y")
    )
    
    pdf = pdfkit.from_string(output, False)
    return pdf
