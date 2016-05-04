import json as simplejson
from cities_light.models import Country, City
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


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
