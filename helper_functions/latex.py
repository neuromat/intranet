# -*- coding: utf-8 -*-
import re
from django.http import HttpResponse
from django.template.loader import render_to_string


def tex_escape(response):
    """
        :param: a plain text message
        :return: the message escaped to appear correctly in LaTeX
    """
    conv = {
        '{ ': '{',
        ' }': '}',
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '<': r'\textless',
        '>': r'\textgreater',
    }

    for key in conv:
        if key in response:
            response = re.sub(key, conv[key], response)

    return response


# Generate latex file from a view path, with a certain context, with the name desired
def generate_latex(tex_view_path, context, filename):
    response = HttpResponse(render_to_string(tex_view_path, context), content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="%s.tex"' % filename
    return response
