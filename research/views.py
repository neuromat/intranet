from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from research.models import MONTHS, YEAR_CHOICES
from django.contrib import messages
from models import ResearchResult
from django.db.models import Q


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