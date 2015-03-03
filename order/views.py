from django.shortcuts import render
from order.models import *
from order.forms import CATEGORY, ORIGIN
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json

# Create your views here.


@login_required
def list_order_by_type(request):
    types = [{'value': order_type[0], 'display': order_type[1].encode('utf-8')} for order_type in ORDER_TYPE]
    status = [{'value': status[0], 'display': status[1].encode('utf-8')} for status in ORDER_STATUS]
    if request.method == 'POST':
        if request.POST['order_type'] == "h":
            status = request.POST.get('status')
            category = request.POST.get('category')
            origin = request.POST.get('origin')
            orders = Order.objects.filter(type_of_order='h', status=status, hardwaresoftware__category=category,
                                          hardwaresoftware__origin=origin)
            context = {'orders': orders}
            return render(request, 'report/list_equipment_supplies_msc.html', context)

        elif request.POST['order_type'] == "s":
            status = request.POST.get('status')
            origin = request.POST.get('origin')
            orders = Order.objects.filter(type_of_order='s', status=status, service__origin=origin)
            context = {'orders': orders}
            return render(request, 'report/list_services.html', context)

        elif request.POST['order_type'] == "e":
            status = request.POST.get('status')
            orders = Order.objects.filter(type_of_order='e', status=status)
            context = {'orders': orders}
            return render(request, 'report/list_events.html', context)

        elif request.POST['order_type'] == "t":
            status = request.POST.get('status')
            orders = Order.objects.filter(type_of_order='t', status=status)
            context = {'orders': orders}
            return render(request, 'report/list_tickets.html', context)

        elif request.POST['order_type'] == "d":
            status = request.POST.get('status')
            orders = Order.objects.filter(type_of_order='d', status=status)
            context = {'orders': orders}
            return render(request, 'report/list_daily_stipend.html', context)

        elif request.POST['order_type'] == "r":
            status = request.POST.get('status')
            orders = Order.objects.filter(type_of_order='r', status=status)
            context = {'orders': orders}
            return render(request, 'report/list_reimbursement.html', context)

    context = {'types': types, 'status': status}
    return render(request, 'report/list_order.html', context)


@login_required
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
    return HttpResponse(json.dumps([categories, origin]), content_type="application/json")
