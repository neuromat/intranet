# -*- coding: utf-8 -*-
import json as simplejson
import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _

from activity.models import ProjectActivities, Seminar, SeminarType
from person.models import Person

from helpers.forms.date_range import DateRangeForm
from helpers.views.date import now_plus_thirty
from helpers.views.latex import generate_latex
from helpers.views.pdf import render as render_to_pdf


def training_programs_search(start_date, end_date):
    return ProjectActivities.objects.filter(
        type_of_activity='t',
        trainingprogram__start_date__gt=start_date,
        trainingprogram__start_date__lt=end_date).order_by('trainingprogram__start_date')


def seminars_search(start_date, end_date, category):
    if category == "All":
        return ProjectActivities.objects.filter(type_of_activity='s',
                                                seminar__date__gt=start_date,
                                                seminar__date__lt=end_date).order_by('-seminar__date')

    return ProjectActivities.objects.filter(type_of_activity='s',
                                            seminar__category=category,
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
def seminars_poster(request):

    speakers = Person.objects.all()
    seminars = ProjectActivities.objects.filter(type_of_activity='s')

    if request.method == 'POST':

        title_id = request.POST['title']

        if title_id is None or title_id == '':
            messages.error(request, _('You have to choose a seminar!'))
            context = {'speakers': speakers, 'seminars': seminars}
            return render(request, 'poster/seminar.html', context)

        try:
            seminar = Seminar.objects.get(id=title_id)
        except Seminar.DoesNotExist:
            raise Http404(_('No seminar matches the given query.'))

        return render_to_pdf('poster/seminar_poster_pdf.html', {'pagesize': 'A4', 'seminar': seminar})

    context = {'speakers': speakers, 'seminars': seminars}
    return render(request, 'poster/seminar.html', context)


@login_required
def seminars_file(request):

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    category = request.GET.get('category')
    extension = request.GET.get('extension')

    seminars = seminars_search(start_date, end_date, category)
    context = {'seminars': seminars}

    if extension == ".tex":
        return generate_latex('report/activity/tex/seminars.tex', context, 'seminars')

    return render_to_pdf('report/activity/pdf/seminars.html', context, 'reports.css')


@login_required
def seminars_show_titles(request):
    if request.method == 'GET':
        speaker_id = request.GET.get('speaker')
        speaker = get_object_or_404(Person, id=speaker_id)

        select = ProjectActivities.objects.filter(type_of_activity='s', seminar__speaker=speaker)
        titles = []
        for title in select:
            titles.append({'pk': title.id, 'valor': title.__str__()})

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
def training_programs_file(request):

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    extension = request.GET.get('extension')

    training_programs = training_programs_search(start_date, end_date)

    context = {'training_programs': training_programs}

    if extension == '.tex':
        return generate_latex('report/activity/tex/training_programs.tex', context, 'training_programs')

    return render_to_pdf('report/activity/pdf/training_programs.html', context, 'reports.css')


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


@login_required
def project_activities_certificate(request):

    people = Person.objects.all()
    persons = people.exclude(signature='')
    project_activities = ProjectActivities.objects.filter(type_of_activity='t') | ProjectActivities.objects.filter(
        type_of_activity='s') | ProjectActivities.objects.filter(type_of_activity='m')

    if request.method == 'POST':
        person_id = request.POST.get('person', None)
        title_id = request.POST['title']
        person_signature_ids = request.POST.getlist('signature', None)
        hours = request.POST['hours']

        if person_id is None or person_id == '':
            messages.error(request, _('You have to choose a person!'))
            context = {'people': people, 'project_activities': project_activities, 'signatures': persons}

        elif title_id is None or title_id == '':
            messages.error(request, _('You have to choose a project activity!'))
            context = {'people': people, 'project_activities': project_activities, 'signatures': persons}

        elif person_signature_ids is None or person_signature_ids == '' or person_signature_ids == ['']:
            messages.error(request, _('You have to choose who will sign the certificate!'))
            context = {'people': people, 'project_activities': project_activities, 'signatures': persons}

        else:

            try:
                person = Person.objects.get(id=person_id)
            except Person.DoesNotExist:
                raise Http404(_('No person matches the given query.'))

            try:
                chosen_activity = ProjectActivities.objects.get(id=title_id)
            except ProjectActivities.DoesNotExist:
                raise Http404(_('No training program matches the given query.'))

            persons = Person.objects.filter(id__in=person_signature_ids)

            if chosen_activity.type_of_activity == 's':
                seminar = chosen_activity.seminar

                #  check if it was at some meeting
                if seminar.belongs_to:

                    meeting = seminar.belongs_to

                    return render_to_pdf(
                        'certificate/pdf/seminar_at_meeting.html',
                        {
                            'pagesize': 'A4',
                            'person': person,
                            'seminar': seminar,
                            'meeting': meeting,
                            'signature': persons,
                            'hours': hours
                        })

                return render_to_pdf(
                    'certificate/pdf/seminar.html',
                    {
                        'pagesize': 'A4',
                        'person': person,
                        'seminar': seminar,
                        'signature': persons,
                        'hours': hours
                    })

            if chosen_activity.type_of_activity == 'm':

                meeting = chosen_activity

                return render_to_pdf(
                    'certificate/pdf/meeting.html',
                    {
                        'pagesize': 'A4',
                        'person': person,
                        'meeting': meeting,
                        'signature': persons,
                        'hours': hours
                    })

            else:  # if chosen_activity.type_of_activity == 't'

                training_program = chosen_activity

                return render_to_pdf(
                    'certificate/pdf/training_program.html',
                    {
                        'pagesize': 'A4',
                        'person': person,
                        'training_program': training_program,
                        'signature': persons,
                        'hours': hours
                    })

        # Common return for the three initial ifs
        return render(request, 'certificate/certificate.html', context)

    context = {'people': people, 'project_activities': project_activities, 'signatures': persons}
    return render(request, 'certificate/certificate.html', context)
