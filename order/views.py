from django.shortcuts import render
from order.models import *

# Create your views here.


def list_order(request):
    latest_order_list = Order.objects.order_by('-date_modified')[:5]
    context = {'latest_order_list': latest_order_list}
    return render(request, 'report/list_order.html', context)