from dal import autocomplete
from cities_light.models import City
from helper_functions.date import *
from scientific_mission.models import ScientificMission
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from helper_functions.latex import generate_latex


class CityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return City.objects.none()

        qs = City.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


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
