import json as simplejson
from dal import autocomplete
from activity.views import render_to_pdf
from cities_light.models import City
from helper_functions.date import *
from scientific_mission.models import ScientificMission
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from helper_functions.latex import generate_latex
from person.models import Person


class CityAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return City.objects.none()

        qs = City.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

@login_required
def anexo5(request):

    people = Person.objects.all()
    missions = ScientificMission.objects.all()

    if request.method == 'POST':

        mission_id = request.POST['title']

        if mission_id is None or mission_id == '':
            messages.error(request, _('You have to choose a scientific mission!'))
            context = {'people': people, 'missions': missions}
            return render(request, 'anexo/anexo5.html', context)
        else:
            try:
                mission = ScientificMission.objects.get(id=mission_id)
            except ScientificMission.DoesNotExist:
                raise Http404(_('No scientific mission matches the given query.'))

            return render_to_pdf(
                'anexo/anexo5_pdf.html',
                {
                    'pagesize': 'A4',
                    'mission': mission,
                    'person': mission.person,
                }
            )

    context = {'people': people, 'missions': missions}
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

        missions = ScientificMission.objects.filter(departure__gt=start_date,
                                                    arrival__lt=end_date).order_by('-departure')

        if end_date >= start_date:
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

    missions = ScientificMission.objects.filter(departure__gt=start_date,
                                                arrival__lt=end_date).order_by('-departure')

    context = {'missions': missions}

    return generate_latex('report/scientific_mission/tex/scientific_missions.tex', context, 'scientific_missions')
