from django.shortcuts import render
from order.models import *

# Create your views here.


def list_order_by_type(request):
    orders = Order.objects.all()

    #if type == 'e':  # Event
        #orders = Order.objects.filter(type_of_order='e')
    #elif type == 'h':  # Equipment / Supplies / Miscellaneous
        #orders = Order.objects.filter(type_of_order='h')
    #elif type == 's':  # Service
        #orders = Order.objects.filter(type_of_order='s')
    #elif type == 't':  # Ticket
        #orders = Order.objects.filter(type_of_order='t')
    #elif type == 'd':  # Daily stipend
        #orders = Order.objects.filter(type_of_order='d')
    #elif type == 'r':  # Reimbursement
        #orders = Order.objects.filter(type_of_order='r')

    context = {'orders': orders}
    return render(request, 'report/list_order.html', context)