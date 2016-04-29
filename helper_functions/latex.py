# -*- coding: utf-8 -*-
import re


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
