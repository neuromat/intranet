# -*- coding: utf-8 -*-
import json as simplejson
import os
import StringIO  # PDF file
from cgi import escape  # PDF file
from xhtml2pdf import pisa  # PDF file
from helper_functions.date import *
from activity.models import ProjectActivities, Seminar, SeminarType
from person.models import Person
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import Context
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO.StringIO()
    path = lambda uri, rel: os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), dest=result, encoding='UTF-8', link_callback=path)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')

    return HttpResponse('_(We had some errors<pre>%s</pre>)' % escape(html))


@login_required
def seminars_report(request):

    categories = SeminarType.objects.all()

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

        category = request.POST['category']

        if category == '0':
            seminars = ProjectActivities.objects.filter(type_of_activity='s',
                                                        seminar__date__gt=start_date,
                                                        seminar__date__lt=end_date).order_by('-seminar__date')
        else:
            seminars = ProjectActivities.objects.filter(type_of_activity='s', seminar__category=category,
                                                        seminar__date__gt=start_date,
                                                        seminar__date__lt=end_date).order_by('-seminar__date')

        if end_date >= start_date:
            context = {'seminars': seminars, 'category': category}
            return render(request, 'report/activity/seminars_report.html', context)
        else:
            messages.error(request, _('End date should be equal or greater than start date.'))
            return render(request, 'report/activity/seminars.html')

    context = {'categories': categories}

    return render(request, 'report/activity/seminars.html', context)


@login_required
def seminar_poster(request):

    speakers = Person.objects.all()
    seminars = ProjectActivities.objects.filter(type_of_activity='s')

    if request.method == 'POST':
        title_id = request.POST['title']

        if title_id is None or title_id == '':
            messages.error(request, _('You have to choose a seminar!'))
            context = {'speakers': speakers, 'seminars': seminars}
            return render(request, 'poster/seminar.html', context)
        else:
            try:
                seminar = Seminar.objects.get(id=title_id)
            except Seminar.DoesNotExist:
                raise Http404(_('No seminar matches the given query.'))

            return render_to_pdf(
                'poster/seminar_poster_pdf.html',
                {
                    'pagesize': 'A4',
                    'seminar': seminar,
                }
            )

    context = {'speakers': speakers, 'seminars': seminars}
    return render(request, 'poster/seminar.html', context)


@login_required
def seminar_show_titles(request):
    if request.method == 'GET':
        speaker_id = request.GET.get('speaker')
        speaker = get_object_or_404(Person, id=speaker_id)

        select = ProjectActivities.objects.filter(type_of_activity='s', seminar__speaker=speaker)
        titles = []
        for title in select:
            titles.append({'pk': title.id, 'valor': title.__unicode__()})

        json = simplejson.dumps(titles)
        return HttpResponse(json, content_type="application/json")


@login_required
def training_programs_report(request):

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

        training_programs = ProjectActivities.objects.filter(type_of_activity='t',
                                                             trainingprogram__start_date__gt=start_date,
                                                             trainingprogram__start_date__lt=end_date).order_by('trainingprogram__start_date')

        if end_date >= start_date:
            context = {'training_programs': training_programs}
            return render(request, 'report/activity/training_programs_report.html', context)
        else:
            messages.error(request, _('End date should be equal or greater than start date.'))
            return render(request, 'report/activity/training_programs.html')

    return render(request, 'report/activity/training_programs.html')


@login_required
def meetings_report(request):

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

        broad_audience = request.POST.get('broad_audience', False)

        meetings = []

        if broad_audience == '0':
            meetings = ProjectActivities.objects.filter(type_of_activity='m', meeting__start_date__gt=start_date,
                                                        meeting__start_date__lt=end_date).order_by('meeting__start_date')

        elif broad_audience == '1':
            meetings = ProjectActivities.objects.filter(type_of_activity='m', meeting__broad_audience='1',
                                                        meeting__start_date__gt=start_date,
                                                        meeting__start_date__lt=end_date).order_by('meeting__start_date')

        elif broad_audience == '2':
            meetings = ProjectActivities.objects.filter(type_of_activity='m', meeting__broad_audience='0',
                                                        meeting__start_date__gt=start_date,
                                                        meeting__start_date__lt=end_date).order_by('meeting__start_date')

        if end_date >= start_date:
            context = {'meetings': meetings}
            return render(request, 'report/activity/meetings_report.html', context)
        else:
            messages.error(request, _('End date should be equal or greater than start date.'))
            return render(request, 'report/activity/meetings.html')

    context = {'cepid_name': settings.CEPID_NAME}
    return render(request, 'report/activity/meetings.html', context)
