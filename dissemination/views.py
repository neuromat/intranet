# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from helpers.views.date import *
from helpers.views.latex import escape_and_generate_latex
from helpers.views.pdf import render as render_to_pdf
from dissemination.models import Dissemination, Internal, InternalMediaOutlet, TYPE_OF_MEDIA


def internal_filter(internal_type, start_date, end_date):
    disseminations = Internal.objects.filter(media_outlet_id=internal_type, date__gte=start_date,
                                             date__lte=end_date).order_by('-date')
    return disseminations


def external_filter(start_date, end_date):
    disseminations = Dissemination.objects.filter(type_of_media='e', date__gte=start_date,
                                                  date__lte=end_date).order_by('-date')
    return disseminations


@login_required
def dissemination_report(request):

    types = [{'value': media_type[0], 'display': media_type[1].encode('utf-8')} for media_type in TYPE_OF_MEDIA]
    internal_types = InternalMediaOutlet.objects.all()
    internal_types = [{'value': media.id, 'display': media.name} for media in internal_types]
    internal_type = ''

    if request.method == 'POST':
        media_type = request.POST['type']

        try:
            if request.POST['start_date'] == '':
                start_date = datetime.datetime.strptime('19700101 00:00:00', '%Y%m%d %H:%M:%S').date()
            else:
                start_date = datetime.datetime.strptime(request.POST['start_date'], "%d/%m/%Y").date()
        except ValueError:
            start_date = False

        try:
            if request.POST['end_date'] == '':
                end_date = now_plus_thirty()
            else:
                end_date = datetime.datetime.strptime(request.POST['end_date'], "%d/%m/%Y").date()
        except ValueError:
            end_date = False

        if media_type != '0':
            if start_date and end_date and end_date >= start_date:
                disseminations = ''
                media_name = ''

                if media_type == 'i':
                    internal_type = request.POST['internal_type']
                    disseminations = internal_filter(internal_type, start_date, end_date)
                    media_name = InternalMediaOutlet.objects.get(id=internal_type).name

                else:
                    disseminations = external_filter(start_date, end_date)
                    media_name = ''

                context = {'start_date': start_date,
                           'end_date': end_date,
                           'disseminations': disseminations,
                           'type': media_type,
                           'media_name': media_name,
                           'internal_type': internal_type}

                return render(request, 'report/dissemination/dissemination_report.html', context)

            else:
                messages.error(request, _('You entered a wrong date format or the end date is not greater than or equal'
                                          ' to the start date.'))

        else:
            messages.error(request, _('You should choose a type.'))

    context = {'types': types, 'internal_types': internal_types}

    return render(request, 'report/dissemination/dissemination.html', context)


@login_required
def dissemination_file(request):

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    media_type = request.GET.get('type')
    internal_type = request.GET.get('internal_type')
    filename = request.GET.get('filename')
    extension = request.GET.get('extension')

    if media_type == 'i':

        disseminations = internal_filter(internal_type, start_date, end_date)
        internal_media = InternalMediaOutlet.objects.get(pk=internal_type)
        media = internal_media.name
        context = {'disseminations': disseminations, 'type': media_type, 'media': media, 'media_name': media,
                   'extension': extension}

    else:

        disseminations = external_filter(start_date, end_date)
        context = {'disseminations': disseminations, 'type': media_type, 'extension': extension}

    if extension == ".tex":
        return escape_and_generate_latex('report/dissemination/tex/disseminations.tex', context, filename, table=True)
    else:
        return render_to_pdf('report/dissemination/pdf/dissemination.html', context, 'reports.css')
