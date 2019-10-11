import os
from io import StringIO, BytesIO

from html import escape
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import get_template

from sistema import settings


def fetch_resources(uri, rel):
    sUrl = settings.STATIC_URL
    sRoot = settings.STATIC_ROOT
    mUrl = settings.MEDIA_URL
    mRoot = settings.MEDIA_ROOT

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )

    return path


def render(template_src, context_dict, css_source=None):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    txt_obj = StringIO(html)
    if css_source:

        pdf = pisa.pisaDocument(txt_obj,
                                dest=result,
                                encoding='UTF-8',
                                link_callback=fetch_resources,
                                default_css=open(os.path.join(settings.BASE_DIR, 'static', 'css', css_source)).read()
                                )
    else:
        pdf = pisa.pisaDocument(txt_obj,
                                dest=result,
                                encoding='UTF-8',
                                link_callback=fetch_resources)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')

    return HttpResponse('_(We had some errors<pre>%s</pre>)' % escape(html))
