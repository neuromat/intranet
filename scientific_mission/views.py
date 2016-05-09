import json as simplejson
from cities_light.models import Country, City
from helper_functions.date import *
from scientific_mission.models import ScientificMission
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from helper_functions.latex import generate_latex


def select_cities(country_field):
    select = City.objects.filter(country_id=country_field)
    cities = []
    for city in select:
        cities.append({'pk': city.id, 'name': city.__unicode__()})

    json = simplejson.dumps(cities)
    return json


@login_required
def load_origin_cities(request):
    if request.method == 'GET':
        origin_country_id = request.GET.get('origin_country')
        origin_country = get_object_or_404(Country, id=origin_country_id)
        result = select_cities(origin_country)

        return HttpResponse(result, content_type="application/json")


@login_required
def load_destination_cities(request):
    if request.method == 'GET':
        destination_country_id = request.GET.get('destination_country')
        destination_country = get_object_or_404(Country, id=destination_country_id)
        result = select_cities(destination_country)

        return HttpResponse(result, content_type="application/json")


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
