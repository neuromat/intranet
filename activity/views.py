# -*- coding: utf-8 -*-
import json as simplejson
import os
import StringIO  # PDF file

from cgi import escape  # PDF file
from helpers.forms.date_range import DateRangeForm
from helpers.views.date import *
from helpers.views.latex import generate_latex
from xhtml2pdf import pisa  # PDF file

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import Context
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _

from activity.models import ProjectActivities, Seminar, SeminarType
from person.models import Person


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


def training_programs_search(start_date, end_date):
    return ProjectActivities.objects.filter(type_of_activity='t',
                                            trainingprogram__start_date__gt=start_date,
                                            trainingprogram__start_date__lt=end_date).order_by(
            'trainingprogram__start_date')


def seminars_search(start_date, end_date, category):
    if category == "All":
        return ProjectActivities.objects.filter(type_of_activity='s',
                                                seminar__date__gt=start_date,
                                                seminar__date__lt=end_date).order_by('-seminar__date')
    else:
        return ProjectActivities.objects.filter(type_of_activity='s', seminar__category=category,
                                                seminar__date__gt=start_date,
                                                seminar__date__lt=end_date).order_by('-seminar__date')


@login_required
def seminars_report(request):

    categories = SeminarType.objects.all()

    if request.method == 'POST':
        category = request.POST['category']

        try:
            if request.POST['start_date'] == '':
                start_date = datetime.datetime.strptime('19700101 00:00:00', '%Y%m%d %H:%M:%S').date()
            else:
                start_date = datetime.datetime.strptime(request.POST['start_date'], "%d/%m/%Y").date()
                start_date -= datetime.timedelta(days=1)
        except ValueError:
            start_date = False

        try:
            if request.POST['end_date'] == '':
                end_date = now_plus_thirty()
            else:
                end_date = datetime.datetime.strptime(request.POST['end_date'], "%d/%m/%Y").date()
                end_date += datetime.timedelta(days=1)
        except ValueError:
            end_date = False

        if start_date and end_date and end_date >= start_date:

            # All seminars
            if category == '0':
                seminars = seminars_search(start_date, end_date, 'All')
                category = "All"

            # Specific category
            else:
                seminars = seminars_search(start_date, end_date, category)

            context = {'start_date': start_date, 'end_date': end_date, 'seminars': seminars, 'category': category}
            return render(request, 'report/activity/seminars_report.html', context)

        else:
            messages.error(request, _('You entered a wrong date format or the end date is not greater than or equal to'
                                      ' the start date.'))

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
def seminar_report(request):

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    category = request.GET.get('category')
    extension = request.GET.get('extension')

    seminars = seminars_search(start_date, end_date, category)
    context = {'seminars': seminars}

    if extension == ".tex":
        return generate_latex('report/activity/tex/seminars.tex', context, 'seminars')
    else:
        return render_to_pdf('report/activity/pdf/seminars.html', context)

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

        form = DateRangeForm(request.POST)

        try:
            if form.data['start_date'] == '':
                start_date = datetime.datetime.strptime('19700101 00:00:00', '%Y%m%d %H:%M:%S').date()
            else:
                start_date = datetime.datetime.strptime(form.data['start_date'], "%d/%m/%Y").date()
                start_date -= datetime.timedelta(days=1)
        except ValueError:
            start_date = False

        try:
            if form.data['end_date'] == '':
                end_date = now_plus_thirty()
            else:
                end_date = datetime.datetime.strptime(form.data['end_date'], "%d/%m/%Y").date()
                end_date += datetime.timedelta(days=1)
        except ValueError:
            end_date = False

        if start_date and end_date and end_date >= start_date:
            training_programs = training_programs_search(start_date, end_date)
            context = {'start_date': start_date, 'end_date': end_date, 'training_programs': training_programs}
            return render(request, 'report/activity/training_programs_report.html', context)
        else:
            messages.error(request, _('You entered a wrong date format or the end date is not greater than or equal to'
                                      ' the start date.'))
    else:
        form = DateRangeForm()

    return render(request, 'report/activity/training_programs.html', {'form': form})


@login_required
def training_programs_latex(request):

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    training_programs = training_programs_search(start_date, end_date)

    context = {'training_programs': training_programs}

    return generate_latex('report/activity/tex/training_programs.tex', context, 'training_programs')


@login_required
def meetings_report(request):

    if request.method == 'POST':
        broad_audience = request.POST.get('broad_audience', False)

        try:
            if request.POST['start_date'] == '':
                start_date = datetime.datetime.strptime('19700101 00:00:00', '%Y%m%d %H:%M:%S').date()
            else:
                start_date = datetime.datetime.strptime(request.POST['start_date'], "%d/%m/%Y").date()
                start_date -= datetime.timedelta(days=1)
        except ValueError:
            start_date = False

        try:
            if request.POST['end_date'] == '':
                end_date = now_plus_thirty()
            else:
                end_date = datetime.datetime.strptime(request.POST['end_date'], "%d/%m/%Y").date()
                end_date += datetime.timedelta(days=1)
        except ValueError:
            end_date = False

        if start_date and end_date and end_date >= start_date:
            meetings = []

            if broad_audience == '0':
                meetings = ProjectActivities.objects.filter(type_of_activity='m', meeting__start_date__gt=start_date,
                                                            meeting__start_date__lt=end_date).\
                    order_by('meeting__start_date')

            elif broad_audience == '1':
                meetings = ProjectActivities.objects.filter(type_of_activity='m', meeting__broad_audience='1',
                                                            meeting__start_date__gt=start_date,
                                                            meeting__start_date__lt=end_date).\
                    order_by('meeting__start_date')

            elif broad_audience == '2':
                meetings = ProjectActivities.objects.filter(type_of_activity='m', meeting__broad_audience='0',
                                                            meeting__start_date__gt=start_date,
                                                            meeting__start_date__lt=end_date).\
                    order_by('meeting__start_date')

            context = {'meetings': meetings}
            return render(request, 'report/activity/meetings_report.html', context)

        else:
            messages.error(request, _('You entered a wrong date format or the end date is not greater than or equal to'
                                      ' the start date.'))

    return render(request, 'report/activity/meetings.html')
