from django.shortcuts import render
from order.models import *
from order.forms import CATEGORY, ORIGIN
from django.http import HttpResponse
import json

# Create your views here.


def list_order_by_type(request):
    orders = [{'value': order[0], 'display': order[1].encode('utf-8')} for order in ORDER_TYPE]
    context = {'orders': orders}
    return render(request, 'report/list_order.html', context)


def select_additional_options(request):
    orders = request.GET.get('order_type')
    if orders == 'h':
        categories = [{'value': category[0], 'display': category[1].encode('utf-8')} for category in CATEGORY]
        origin = [{'value': orig[0], 'display': orig[1].encode('utf-8')} for orig in ORIGIN]
    elif orders == 's':
        origin = [{'value': orig[0], 'display': orig[1].encode('utf-8')} for orig in ORIGIN]
        categories = []
    else:
        categories = []
        origin = []
    return HttpResponse(json.dumps([categories,origin]), content_type="application/json")
