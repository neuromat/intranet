import datetime
import json as simplejson
from activity.views import render_to_pdf
from cities_light.models import City
from configuration.models import ProcessNumber
from dal import autocomplete
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from helpers.views.date import *
from helpers.views.latex import generate_latex
from helpers.views.extenso import dExtenso
from person.models import Person
from scientific_mission.models import ScientificMission, Route


class CityAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated():
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

            if mission:
                routes = Route.objects.filter(scientific_mission=mission).order_by('order')

                if routes:

                    start_date = routes.first()
                    end_date = routes.last()
                else:
                    messages.error(request, _("You should've set routes for this mission."))
                    context = {'people': people, 'missions': missions, 'default_date': date, 'process': process}
                    return render(request, 'anexo/anexo5.html', context)

            ext = dExtenso()
            amount = str(int(mission.amount_paid))
            cents = str(mission.amount_paid - int(mission.amount_paid))[2:4]  # Only two digits in cents
            amount = ext.getExtenso(amount)
            cents = ext.getExtenso(cents)

            try:
                people = Person.objects.all()
                principal_investigator = people.get(role__name="Principal Investigator")
            except:
                messages.error(request, _('You must set a person with the role of Principal Investigator.'))
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
                    'mission': mission,
                    'pagesize': 'A4',
                    'person': mission.person,
                    'process': process,
                    'principal_investigator': principal_investigator,
                    'routes': routes,
                    'start_date': start_date.departure,
                }
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
def mission_show_titles(request):
    if request.method == 'GET':
        person_id = request.GET.get('person')
        person = get_object_or_404(Person, id=person_id)

        missions = ScientificMission.objects.filter(person=person)
        titles = []

        for title in missions:
            titles.append({'pk': title.id, 'valor': title.__unicode__()})

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

        if end_date >= start_date:
            missions = get_missions(start_date, end_date)
            context = {'start_date': start_date, 'end_date': end_date, 'missions': missions}
            return render(request, 'report/scientific_mission/scientific_missions_report.html', context)
        else:
            messages.error(request, 'End date should be equal or greater than start date.')
            return render(request, 'report/scientific_mission/scientific_missions.html')

    return render(request, 'report/scientific_mission/scientific_missions.html')


@login_required
def missions_tex(request):

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    missions = get_missions(datetime.datetime.strptime(start_date, "%Y-%m-%d").date(),
                            datetime.datetime.strptime(end_date, "%Y-%m-%d").date())

    context = {'missions': missions}

    return generate_latex('report/scientific_mission/tex/scientific_missions.tex', context, 'scientific_missions')
