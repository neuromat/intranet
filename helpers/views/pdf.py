import os
import StringIO

from cgi import escape
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template

from sistema import settings


def fetch_resources(uri, rel):

    # use short variable names
    base = settings.BASE_DIR
    sUrl = settings.STATIC_URL  # Typically /static/
    sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL  # Typically /static/media/
    mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = base + os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = base + os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )

    return path


def render(template_src, context_dict, css_source=None):
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO.StringIO()

    if css_source:
        pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")),
                                dest=result,
                                encoding='UTF-8',
                                link_callback=fetch_resources,
                                default_css=open(os.path.join(settings.BASE_DIR, 'static', 'css', css_source)).read())
    else:
        pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")),
                                dest=result,
                                encoding='UTF-8',
                                link_callback=fetch_resources)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')

    return HttpResponse('_(We had some errors<pre>%s</pre>)' % escape(html))
