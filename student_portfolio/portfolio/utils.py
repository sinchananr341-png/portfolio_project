from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

try:
    from xhtml2pdf import pisa
    HAS_XHTML2PDF = True
except ImportError:
    HAS_XHTML2PDF = False


def render_to_pdf(template_src, context_dict={}):
    """Render an HTML template to a PDF HttpResponse."""
    if not HAS_XHTML2PDF:
        return None

    template = get_template(template_src)
    html = template.render(context_dict)
    
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="resume.pdf"'
        return response
    return None
