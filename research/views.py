from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from research.models import MONTHS, YEAR_CHOICES
from django.contrib import messages
from models import ResearchResult, AcademicWork, TypeAcademicWork
from django.db.models import Q
import datetime

TIME = " 00:00:00"

def start_date_typed(start_date):
    start_day = start_date[0:2]
    start_month = start_date[3:5]
    start_year = start_date[6:10]
    start_date = start_year+start_month+start_day+TIME
    start_date = datetime.datetime.strptime(start_date, "%Y%m%d %H:%M:%S").date()
    start_date -= datetime.timedelta(days=1)
    return start_date


def end_date_typed(end_date):
    end_day = end_date[0:2]
    end_month = end_date[3:5]
    end_year = end_date[6:10]
    end_date = end_year+end_month+end_day+TIME
    end_date = datetime.datetime.strptime(end_date, "%Y%m%d %H:%M:%S").date()
    end_date += datetime.timedelta(days=1)
    return end_date


def now_plus_five_years():
    date = datetime.datetime.now() + datetime.timedelta(days=5*365)
    date = date.strftime("%Y%m%d %H:%M:%S")
    date = datetime.datetime.strptime(date, '%Y%m%d %H:%M:%S').date()
    return date


@login_required
def published_articles(request):

    months = [{'value': month[0], 'display': month[1]} for month in MONTHS.items()]
    years = [{'value': year[0], 'display': year[1]} for year in YEAR_CHOICES]

    if request.method == 'POST':
        start_month = request.POST['start_month']
        start_year = request.POST['start_year']
        end_month = request.POST['end_month']
        end_year = request.POST['end_year']

        if start_month == '0' and start_year == '0' and end_month == '0' and end_year == '0':
            published = ResearchResult.objects.filter(Q(published__published_type='a') |
                                                      Q(published__published_type='m')).order_by('year')
        else:
            published = ResearchResult.objects.filter(Q(published__published_type='a') |
                                                      Q(published__published_type='m'),
                                                      month__gte=start_month, year__gte=start_year,
                                                      month__lte=end_month, year__lte=end_year).order_by('year')

        if start_year < end_year:
            context = {'published': published}
            return render(request, 'report/research/published_report.html', context)
        elif start_year == end_year and start_month <= end_month:
            context = {'published': published}
            return render(request, 'report/research/published_report.html', context)
        else:
            messages.error(request, _('The end date must be equal or greater than start date.'))
            context = {'months': months, 'years': years}
            return render(request, 'report/research/published.html', context)

    context = {'months': months, 'years': years}
    return render(request, 'report/research/published.html', context)


@login_required
def academic_works(request):

    types = TypeAcademicWork.objects.all()

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
            end_date = now_plus_five_years()

        type = request.POST['type']

        results = AcademicWork.objects.filter(type=type, start_date__gt=start_date,
                                              end_date__lt=end_date).order_by('end_date')

        if end_date >= start_date:
            context = {'results': results, 'type': type}
            return render(request, 'report/research/academic_works_report.html', context)
        else:
            messages.error(request, _('End date should be equal or greater than start date.'))
            context = {'types': types}
            return render(request, 'report/research/academic_works.html', context)

    context = {'types': types}

    return render(request, 'report/research/academic_works.html', context)