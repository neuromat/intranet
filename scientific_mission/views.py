import json as simplejson
from activity.views import render_to_pdf
from cities_light.models import City
from dal import autocomplete
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from helper_functions.date import *
from helper_functions.latex import generate_latex
from helper_functions.extenso import dExtenso
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
            process = '2013/07699-0'

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

            ext = dExtenso()
            amount = str(int(mission.amount_paid))
            cents = str(mission.amount_paid - int(mission.amount_paid))[2:4]  # Apenas dois digitos nos centavos
            amount = ext.getExtenso(amount)
            cents = ext.getExtenso(cents)

            return render_to_pdf(
                'anexo/anexo5_pdf.html',
                {
                    'pagesize': 'A4',
                    'mission': mission,
                    'person': mission.person,
                    'date': date,
                    'process': process,
                    'amount': amount,
                    'cents': cents,
                }
            )

    date = datetime.datetime.now()
    process = '2013/07699-0'
    context = {'people': people, 'missions': missions, 'default_date': date, 'process': process}
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
