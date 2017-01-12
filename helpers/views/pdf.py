import os
import StringIO

from cgi import escape
from xhtml2pdf import pisa
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template


def render(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO.StringIO()
    path = lambda uri, rel: os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), dest=result, encoding='UTF-8', link_callback=path)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')

    return HttpResponse('_(We had some errors<pre>%s</pre>)' % escape(html))
