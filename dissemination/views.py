# -*- coding: utf-8 -*-
from helper_functions.date import *
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from dissemination.models import Dissemination, Internal, InternalMediaOutlet, TYPE_OF_MEDIA
from django.utils.translation import ugettext_lazy as _


@login_required
def dissemination_report(request):

    types = [{'value': type[0], 'display': type[1].encode('utf-8')} for type in TYPE_OF_MEDIA]
    internal_types = InternalMediaOutlet.objects.all()
    internal_types = [{'value': type.id, 'display': type.name} for type in internal_types]

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
            disseminations = Internal.objects.filter(media_outlet_id=internal_type, date__gt=start_date,
                                                     date__lt=end_date).order_by('-date')

        else:
            disseminations = Dissemination.objects.filter(type_of_media='e', date__gt=start_date,
                                                          date__lt=end_date).order_by('-date')

        if end_date >= start_date:
            context = {'disseminations': disseminations, 'type': type}
            return render(request, 'report/dissemination/dissemination_report.html', context)
        else:
            context = {'types': types, 'internal_types': internal_types}
            messages.error(request, _('End date should be equal or greater than start date.'))
            return render(request, 'report/dissemination/dissemination.html', context)

    context = {'types': types, 'internal_types': internal_types}

    return render(request, 'report/dissemination/dissemination.html', context)