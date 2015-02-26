from django.shortcuts import render
from order.models import *
from order.forms import CATEGORY
from django.http import HttpResponse
import json

# Create your views here.


def list_order_by_type(request):
    orders = [{'value': order[0], 'display': order[1].encode('utf-8')} for order in ORDER_TYPE]
    context = {'orders': orders}
    return render(request, 'report/list_order.html', context)


def selected_categories(request):
    orders = request.GET.get('order_type')
    if orders == 'h':
        categories = [{'value': category[0], 'display': category[1].encode('utf-8')} for category in CATEGORY]
    else:
        categories = []
    return HttpResponse(json.dumps(categories), content_type="application/json")

