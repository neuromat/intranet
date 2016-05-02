# -*- coding: utf-8 -*-
from helper_functions.date import *
from helper_functions.latex import *
from dissemination.models import Dissemination, Internal, InternalMediaOutlet, TYPE_OF_MEDIA
from django.shortcuts import render, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string


@login_required
def dissemination_report(request):

    types = [{'value': type[0], 'display': type[1].encode('utf-8')} for type in TYPE_OF_MEDIA]
    internal_types = InternalMediaOutlet.objects.all()
    internal_types = [{'value': type.id, 'display': type.name} for type in internal_types]
    internal_type = ''

    if request.method == 'POST':

        start_date = request.POST['start_date']

        if start_date:
            start_date = start_date_typed(start_date)
        else:
            start_date = datetime.datetime.strptime('19700101 00:00:00', '%Y%m%d %H:%M:%S').date()

        end_date = request.POST['end_date']

        if end_date:
            end_date = end_date_typed(end_date)
        else:
            end_date = now_plus_thirty()

        type = request.POST['type']

        if type == 'i':
            internal_type = request.POST['internal_type']
            disseminations = internal_filter(internal_type, start_date, end_date)
            media_name = InternalMediaOutlet.objects.get(id=internal_type).name

        else:
            disseminations = external_filter(start_date, end_date)
            media_name = ''

        if end_date >= start_date:
            context = {'start_date': start_date,
                       'end_date': end_date,
                       'disseminations': disseminations,
                       'type': type,
                       'media_name': media_name,
                       'internal_type': internal_type}
            return render(request, 'report/dissemination/dissemination_report.html', context)
        else:
            context = {'types': types, 'internal_types': internal_types}
            messages.error(request, _('End date should be equal or greater than start date.'))
            return render(request, 'report/dissemination/dissemination.html', context)

    context = {'types': types, 'internal_types': internal_types}

    return render(request, 'report/dissemination/dissemination.html', context)


def dissemination_tex(request):

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    type = request.GET.get('type')
    internal_type = request.GET.get('internal_type')

    if type == 'i':
        disseminations = internal_filter(internal_type, start_date, end_date)

    else:
        disseminations = external_filter(start_date, end_date)

    context = {'disseminations': disseminations, 'type': type}

    response = render_to_string('report/dissemination/tex/disseminations.tex', context)
    response = tex_escape(response)

    latex_response = HttpResponse(response, content_type='text/plain')
    latex_response['Content-Disposition'] = 'attachment; filename="disseminations.tex"'

    return latex_response


def internal_filter(internal_type, start_date, end_date):
    disseminations = Internal.objects.filter(media_outlet_id=internal_type, date__gt=start_date,
                                                     date__lt=end_date).order_by('-date')
    return disseminations


def external_filter(start_date, end_date):
    disseminations = Dissemination.objects.filter(type_of_media='e', date__gt=start_date,
                                                          date__lt=end_date).order_by('-date')
    return disseminations
