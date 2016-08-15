# -*- coding: utf-8 -*-
from helpers.views.date import *
from helpers.views.latex import escape_and_generate_latex
from dissemination.models import Dissemination, Internal, InternalMediaOutlet, TYPE_OF_MEDIA
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _


def internal_filter(internal_type, start_date, end_date):
    disseminations = Internal.objects.filter(media_outlet_id=internal_type, date__gt=start_date,
                                             date__lt=end_date).order_by('-date')
    return disseminations


def external_filter(start_date, end_date):
    disseminations = Dissemination.objects.filter(type_of_media='e', date__gt=start_date,
                                                  date__lt=end_date).order_by('-date')
    return disseminations


@login_required
def dissemination_report(request):

    types = [{'value': media_type[0], 'display': media_type[1].encode('utf-8')} for media_type in TYPE_OF_MEDIA]
    internal_types = InternalMediaOutlet.objects.all()
    internal_types = [{'value': media.id, 'display': media.name} for media in internal_types]
    internal_type = ''

    if request.method == 'POST':

        media_type = request.POST['type']

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

        # Internal, external or no type selected
        type_selected = True
        if media_type == 'i':
            internal_type = request.POST['internal_type']
            disseminations = internal_filter(internal_type, start_date, end_date)
            media_name = InternalMediaOutlet.objects.get(id=internal_type).name

        elif media_type == 'e':
            disseminations = external_filter(start_date, end_date)
            media_name = ''

        else:
            type_selected = False

        if type_selected:
            if end_date >= start_date:
                context = {'start_date': start_date,
                           'end_date': end_date,
                           'disseminations': disseminations,
                           'type': media_type,
                           'media_name': media_name,
                           'internal_type': internal_type}
                return render(request, 'report/dissemination/dissemination_report.html', context)
            else:
                context = {'types': types, 'internal_types': internal_types}
                messages.error(request, _('End date should be equal or greater than start date.'))
                return render(request, 'report/dissemination/dissemination.html', context)
        else:
            messages.error(request, _('You should choose a type.'))

    context = {'types': types, 'internal_types': internal_types}

    return render(request, 'report/dissemination/dissemination.html', context)


@login_required
def dissemination_tex(request):

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    media_type = request.GET.get('type')
    internal_type = request.GET.get('internal_type')
    filename = request.GET.get('filename')

    if media_type == 'i':
        disseminations = internal_filter(internal_type, start_date, end_date)
        internal_media = InternalMediaOutlet.objects.get(pk=internal_type)
        media = internal_media.name
        context = {'disseminations': disseminations, 'type': media_type, 'media': media}

    else:
        disseminations = external_filter(start_date, end_date)
        context = {'disseminations': disseminations, 'type': media_type}

    return escape_and_generate_latex('report/dissemination/tex/disseminations.tex', context, filename, table=True)
