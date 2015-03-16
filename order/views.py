from django.shortcuts import render
from order.models import *
from member.models import University
from order.forms import CATEGORY, ORIGIN
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import json as simplejson
import json

# Create your views here.


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


def show_department(request):
    if request.method == 'GET':
        institute_id = request.GET.get('institute')
        institute = get_object_or_404(Institute, id=institute_id)

        select = Department.objects.filter(institute=institute)
        department = []
        for dep in select:
            department.append({'pk': dep.id, 'valor': dep.__unicode__()})

        json = simplejson.dumps(department)
        return HttpResponse(json, content_type="application/json")


@login_required
def scientific_missions_report(request):
    orders = Order.objects.filter(type_of_order='d', status='f')
    context = {'orders': orders}
    return render(request, 'report/scientific_missions.html', context)


@login_required
def list_order_by_type(request):
    types = [{'value': order_type[0], 'display': order_type[1].encode('utf-8')} for order_type in ORDER_TYPE]

    if request.method == 'POST':

        if request.POST['order_type'] == "h":
            status = request.POST.get('status')
            category = request.POST.get('category')
            origin = request.POST.get('origin')
            if status == '' and category == '' and origin == '':
                orders = Order.objects.filter(type_of_order='h')
            elif status == '' and category == '':
                orders = Order.objects.filter(type_of_order='h', hardwaresoftware__origin=origin)
            elif status == '' and origin == '':
                orders = Order.objects.filter(type_of_order='h', hardwaresoftware__category=category)
            elif category == '' and origin == '':
                orders = Order.objects.filter(type_of_order='h', status=status)
            elif status == '':
                orders = Order.objects.filter(type_of_order='h', hardwaresoftware__origin=origin,
                                              hardwaresoftware__category=category)
            elif category == '':
                orders = Order.objects.filter(type_of_order='h', status=status, hardwaresoftware__origin=origin)
            elif origin == '':
                orders = Order.objects.filter(type_of_order='h', status=status, hardwaresoftware__category=category)
            else:
                orders = Order.objects.filter(type_of_order='h', status=status, hardwaresoftware__category=category,
                                              hardwaresoftware__origin=origin)

            context = {'orders': orders, 'status': status, 'category': category, 'origin': origin}
            return render(request, 'report/list_equipment_supplies_msc.html', context)

        elif request.POST['order_type'] == "s":
            status = request.POST.get('status')
            origin = request.POST.get('origin')
            if status == '' and origin == '':
                orders = Order.objects.filter(type_of_order='s')
            elif status == '':
                orders = Order.objects.filter(type_of_order='s', service__origin=origin)
            elif origin == '':
                orders = Order.objects.filter(type_of_order='s', status=status)
            else:
                orders = Order.objects.filter(type_of_order='s', status=status, service__origin=origin)

            context = {'orders': orders}
            return render(request, 'report/list_services.html', context)

        elif request.POST['order_type'] == "e":
            status = request.POST.get('status')
            if status == '':
                orders = Order.objects.filter(type_of_order='e')
            else:
                orders = Order.objects.filter(type_of_order='e', status=status)

            context = {'orders': orders}
            return render(request, 'report/list_events.html', context)

        elif request.POST['order_type'] == "t":
            status = request.POST.get('status')
            if status == '':
                orders = Order.objects.filter(type_of_order='t')
            else:
                orders = Order.objects.filter(type_of_order='t', status=status)

            context = {'orders': orders}
            return render(request, 'report/list_tickets.html', context)

        elif request.POST['order_type'] == "d":
            status = request.POST.get('status')
            if status == '':
                orders = Order.objects.filter(type_of_order='d')
            else:
                orders = Order.objects.filter(type_of_order='d', status=status)

            context = {'orders': orders}
            return render(request, 'report/list_daily_stipend.html', context)

        elif request.POST['order_type'] == "r":
            status = request.POST.get('status')
            if status == '':
                orders = Order.objects.filter(type_of_order='r')
            else:
                orders = Order.objects.filter(type_of_order='r', status=status)

            context = {'orders': orders}
            return render(request, 'report/list_reimbursement.html', context)

    context = {'types': types}
    return render(request, 'report/list_order.html', context)


@login_required
def select_additional_options(request):
    orders = request.GET.get('order_type')
    if orders == 'h':
        status = [{'value': status[0], 'display': status[1].encode('utf-8')} for status in ORDER_STATUS]
        categories = [{'value': category[0], 'display': category[1].encode('utf-8')} for category in CATEGORY]
        origin = [{'value': orig[0], 'display': orig[1].encode('utf-8')} for orig in ORIGIN]
    elif orders == 's':
        status = [{'value': status[0], 'display': status[1].encode('utf-8')} for status in ORDER_STATUS]
        origin = [{'value': orig[0], 'display': orig[1].encode('utf-8')} for orig in ORIGIN]
        categories = []
    else:
        status = [{'value': status[0], 'display': status[1].encode('utf-8')} for status in ORDER_STATUS]
        categories = []
        origin = []
    return HttpResponse(json.dumps([status, categories, origin]), content_type="application/json")