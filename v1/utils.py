import jinja2
import pdfkit

from django.conf import settings


def render_mail(data):
    template_folder = str(settings.BASE_DIR) + '/mail_templates'
    template_loader = jinja2.FileSystemLoader(template_folder)
    template_env = jinja2.Environment(loader=template_loader)
    template_name = 'skl.html'
    template = template_env.get_template(template_name)
    output = template.render(surat=data)

    pdf = pdfkit.from_string(output, False)
    return pdf
