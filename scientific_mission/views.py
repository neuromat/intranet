from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_http_methods

import json as simplejson

from dal import autocomplete
from cities_light.models import City

from helpers.views.pdf import render as render_to_pdf
from helpers.views.principal_investigator import principal_investigator_name
from helpers.forms.date_range import DateRangeForm
from helpers.views.date import now_plus_thirty
from helpers.views.latex import generate_latex
from helpers.views.extenso import dExtenso

from configuration.models import ProcessNumber
from person.models import Person

from scientific_mission.models import ScientificMission, Route
from scientific_mission.forms import AnnexSixForm, AnnexSevenForm, AnnexNineForm
from scientific_mission.forms import annex_seven_choices as choices


class CityAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return City.objects.none()

        qs = City.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


def date_typed(date):
    day = date[0:2]
    month = date[3:5]
    year = date[6:10]
    date = year+month+day
    date = datetime.datetime.strptime(date, "%Y%m%d").date()
    return date


def money_to_strings(value):
    ext = dExtenso()
    amount = str(int(value))
    cents = str(value - int(value))[2:4]  # Only two digits in cents
    amount = ext.getExtenso(amount)
    cents = ext.getExtenso(cents)
    return amount, cents


@login_required
def anexo5(request):

    people = Person.objects.all()
    missions = ScientificMission.objects.all()

    if request.method == 'POST':

        mission_id = request.POST['title']
        process = request.POST['process']
        date = request.POST['issue_date']

        if date:
            date = date_typed(date)
        else:
            date = datetime.datetime.now()

        if not process:
            process = ProcessNumber.get_solo()
            process = process.process_number

            if process == '0000/00000-0':
                messages.info(request, mark_safe(_('You should have configured your process number on configurations. '
                                                   ' Click <a href="../../configuration">here</a> to configure it.')))

        if mission_id is None or mission_id == '':

            messages.error(request, _('You have to choose a scientific mission!'))
            date = datetime.datetime.now()
            context = {'people': people, 'missions': missions, 'default_date': date, 'process': process}
            return render(request, 'anexo/anexo5.html', context)

        else:

            try:
                mission = ScientificMission.objects.get(id=mission_id)
            except ScientificMission.DoesNotExist:
                raise Http404(_('No scientific mission matches the given query.'))

            routes = None
            start_date = None
            end_date = None

            routes = Route.objects.filter(scientific_mission=mission).order_by('order')

            if routes:
                start_date = routes.first()
                end_date = routes.last()
            else:
                messages.error(request, _("You should've set routes for this mission."))
                context = {'people': people, 'missions': missions, 'default_date': date, 'process': process}
                return render(request, 'anexo/anexo5.html', context)

            amount, cents = money_to_strings(mission.amount_paid)

            principal_investigator = principal_investigator_name()

            if principal_investigator is None:
                messages.error(request, _('You must set the Principal Investigator.'))
                date = datetime.datetime.now()
                context = {'people': people, 'missions': missions, 'default_date': date, 'process': process}
                return render(request, 'anexo/anexo5.html', context)

            return render_to_pdf(
                'anexo/anexo5_pdf.html',
                {
                    'amount': amount,
                    'cents': cents,
                    'date': date,
                    'end_date': end_date.departure,
                    'value': mission.amount_paid,
                    'pagesize': 'A4',
                    'person': mission.person,
                    'process': process,
                    'principal_investigator': principal_investigator,
                    'routes': routes,
                    'start_date': start_date.departure,
                },
                'anexo.css',
            )

    date = datetime.datetime.now()
    process = ProcessNumber.get_solo()
    process_number = process.process_number

    if process_number == '0000/00000-0':
        messages.info(request, mark_safe(_('You should have configured your process number on configurations. '
                                           ' Click <a href="../../configuration">here</a> to configure it.')))

    context = {'people': people, 'missions': missions, 'default_date': date, 'process': process_number}
    return render(request, 'anexo/anexo5.html', context)


@login_required
def anexo6(request):

    if request.method == 'POST':

        principal_investigator = principal_investigator_name()

        if principal_investigator is None:
            messages.error(request, _('You must set the Principal Investigator.'))
            return render(request, 'anexo/anexo6.html', {'form': AnnexSixForm()})

        form = AnnexSixForm(request.POST)

        if form.is_valid():

            value = form.cleaned_data['value']
            amount, cents = money_to_strings(value)
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            person = principal_investigator
            process = form.cleaned_data['process']

            if not process:
                process = ProcessNumber.get_solo()
                process = process.process_number

                if process == '0000/00000-0':
                    messages.info(request,
                                  mark_safe(_('You should have configured your process number on configurations. '
                                              ' Click <a href="../../configuration">here</a> to configure it.')))

            return render_to_pdf(
                'anexo/anexo6_pdf.html',
                {
                    'value': value,
                    'amount': amount,
                    'cents': cents,
                    'person': person,
                    'start_date': start_date,
                    'end_date': end_date,
                    'process': process,
                    'date': datetime.datetime.now(),
                },
                'anexo.css'
            )

        else:

            messages.error(request, mark_safe(_('Your form is not valid.')))

            form = AnnexSixForm()
            return render(request, 'anexo/anexo6.html', {'form': form})

    else:

        form = AnnexSixForm()

    return render(request, 'anexo/anexo6.html', {'form': form})


@login_required
def anexo7(request):

    people = Person.objects.all()

    if request.method == 'POST':

        form = AnnexSevenForm(request.POST)

        if form.is_valid():

            choice = form.cleaned_data['choice']
            value = form.cleaned_data['value']
            person = form.cleaned_data['person']
            process = form.cleaned_data['process']
            reimbursement = form.cleaned_data['reimbursement']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            stretch = form.cleaned_data['stretch']

            amount, cents = money_to_strings(value)

            if not process:
                process = ProcessNumber.get_solo()
                process = process.process_number

                if process == '0000/00000-0':
                    messages.info(request,
                                  mark_safe(_('You should have configured your process number on configurations. '
                                              ' Click <a href="../../configuration">here</a> to configure it.')))

            principal_investigator = principal_investigator_name()

            if principal_investigator is None:
                messages.error(request, _('You must set the Principal Investigator.'))
                return render(request, 'anexo/anexo7.html', {'people': people,
                                                             'default_date': datetime.datetime.now(),
                                                             'process': process})

            return render_to_pdf(
                'anexo/anexo7_pdf.html',
                {
                    'reimbursement': choices[int(reimbursement)][1],
                    'value': value,
                    'amount': amount,
                    'cents': cents,
                    'choice': choice,
                    'start_date': start_date,
                    'end_date': end_date,
                    'stretch': stretch,
                    'person': person,
                    'process': process,
                    'principal_investigator': principal_investigator,
                    'date': datetime.datetime.now(),
                },
                'anexo.css'
            )

        else:

            messages.info(request,
                          mark_safe(_('Your form is not valid.')))

            form = AnnexSevenForm()
            return render(request, 'anexo/anexo7.html', {'form': form})

    else:

        form = AnnexSevenForm()

    return render(request, 'anexo/anexo7.html', {'form': form})


@login_required
def anexo9(request):

    people = Person.objects.all()

    if request.method == 'POST':

        form = AnnexNineForm(request.POST)

        if form.is_valid():

            value = form.cleaned_data['value']
            person = form.cleaned_data['person']
            note = form.cleaned_data['note']
            process = form.cleaned_data['process']
            service_provided = form.cleaned_data['job']

            amount, cents = money_to_strings(value)

            if not process:
                process = ProcessNumber.get_solo()
                process = process.process_number

                if process == '0000/00000-0':
                    messages.info(request,
                                  mark_safe(_('You should have configured your process number on configurations. '
                                              ' Click <a href="../../configuration">here</a> to configure it.')))

            principal_investigator = principal_investigator_name()

            if principal_investigator is None:
                messages.error(request, _('You must set the Principal Investigator.'))
                return render(request, 'anexo/anexo9.html', {'people': people,
                                                             'default_date': datetime.datetime.now(),
                                                             'process': process})

            return render_to_pdf(
                'anexo/anexo9_pdf.html',
                {
                    'value': value,
                    'amount': amount,
                    'cents': cents,
                    'note': note,
                    'person': person,
                    'process': process,
                    'principal_investigator': principal_investigator,
                    'service_provided': service_provided,
                    'date': datetime.datetime.now(),
                },
                'anexo.css'
            )

        else:

            messages.info(request,
                          mark_safe(_('Your form is not valid.')))

            form = AnnexNineForm()
            return render(request, 'anexo/anexo9.html', {'form': form})

    else:

        form = AnnexNineForm()

    return render(request, 'anexo/anexo9.html', {'form': form})


@login_required
@require_http_methods(["GET"])
def mission_show_titles(request):
    person_id = request.GET.get('person')
    person = get_object_or_404(Person, id=person_id)

    missions = ScientificMission.objects.filter(person=person)
    titles = []

    for title in missions:
        titles.append({'pk': title.id, 'valor': title.__str__()})

    json = simplejson.dumps(titles)
    return HttpResponse(json, content_type="application/json")


def get_missions(start_date, end_date):
    missions = []
    for mission in ScientificMission.objects.all():
        routes = Route.objects.filter(scientific_mission=mission).order_by('order')
        if routes:
            departure = routes.first()
            arrival = routes.last()

            if departure.departure.date() >= start_date and arrival.departure.date() <= end_date:
                valid_mission = {'mission': mission, 'departure': departure, 'arrival': arrival}
                missions.append(valid_mission)

    return missions


@login_required
def missions_report(request):

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
            missions = get_missions(start_date, end_date)
            context = {'start_date': start_date, 'end_date': end_date, 'missions': missions}
            return render(request, 'report/scientific_mission/scientific_missions_report.html', context)
        else:
            messages.error(request, _('You entered a wrong date format or the end date is not greater than or equal to'
                                      ' the start date.'))

    else:
        form = DateRangeForm()
        args = {}
        args['form'] = form

    return render(request, 'report/scientific_mission/scientific_missions.html', {'form': form})


@login_required
def missions_file(request):

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    extension = request.GET.get('extension')

    missions = get_missions(datetime.datetime.strptime(start_date, "%Y-%m-%d").date(),
                            datetime.datetime.strptime(end_date, "%Y-%m-%d").date())

    context = {'start_date': start_date, 'end_date': end_date, 'missions': missions}

    if extension == ".tex":
        return generate_latex('report/scientific_mission/tex/scientific_missions.tex', context, 'scientific_missions')
    else:
        return render_to_pdf('report/scientific_mission/pdf/scientific_missions.html', context, 'reports.css')
