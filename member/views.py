from member.models import University, Institute
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import json as simplejson


@login_required
def show_institute(request):
    if request.method == 'GET':
        university_id = request.GET.get('university')
        university = get_object_or_404(University, id=university_id)

        select = Institute.objects.filter(university=university)
        institute = []
        for inst in select:
            institute.append({'pk': inst.id, 'valor': inst.__unicode__()})

        json = simplejson.dumps(institute)
        return HttpResponse(json, content_type="application/json")
