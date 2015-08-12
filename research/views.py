from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from models import ResearchResult, AcademicWork, TypeAcademicWork
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
def articles(request):

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

        scientific = ResearchResult.objects.filter(published__published_type='a', team='s',
                                                   published__article__date__gt=start_date,
                                                   published__article__date__lt=end_date).order_by('-published__article__date')

        dissemination = ResearchResult.objects.filter(published__published_type='a', team='d',
                                                      published__article__date__gt=start_date,
                                                      published__article__date__lt=end_date).order_by('-published__article__date')

        transfer = ResearchResult.objects.filter(published__published_type='a', team='t',
                                                 published__article__date__gt=start_date,
                                                 published__article__date__lt=end_date).order_by('-published__article__date')

        # "c" means Communication. Refers to communications in meetings with referee.
        c_scientific = ResearchResult.objects.filter(published__published_type='m', team='s',
                                                     published__communicationinmeeting__event__start_date__gt=start_date,
                                                     published__communicationinmeeting__event__start_date__lt=end_date).order_by('-published__communicationinmeeting__event__start_date')

        c_dissemination = ResearchResult.objects.filter(published__published_type='m', team='d',
                                                        published__communicationinmeeting__event__start_date__gt=start_date,
                                                        published__communicationinmeeting__event__start_date__lt=end_date).order_by('-published__communicationinmeeting__event__start_date')

        c_transfer = ResearchResult.objects.filter(published__published_type='m', team='t',
                                                   published__communicationinmeeting__event__start_date__gt=start_date,
                                                   published__communicationinmeeting__event__start_date__lt=end_date).order_by('-published__communicationinmeeting__event__start_date')

        submitted = ResearchResult.objects.filter(research_result_type='u', unpublished__type='a',
                                                  unpublished__paper_status='s', unpublished__status='i',
                                                  unpublished__date__gt=start_date,
                                                  unpublished__date__lt=end_date).order_by('-unpublished__date')

        draft = ResearchResult.objects.filter(research_result_type='u', unpublished__type='a',
                                              unpublished__paper_status='d', unpublished__status='i',
                                              unpublished__date__gt=start_date,
                                              unpublished__date__lt=end_date).order_by('-unpublished__date')

        if start_date < end_date:
            context = {'scientific': scientific, 'dissemination': dissemination, 'transfer': transfer,
                       'c_scientific': c_scientific, 'c_dissemination': c_dissemination, 'c_transfer': c_transfer,
                       'submitted': submitted, 'draft': draft}
            return render(request, 'report/research/articles_report.html', context)

    return render(request, 'report/research/articles.html')


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

        work_type = request.POST['type']

        # Show all the academic works completed within the selected period
        result_status_concluded = AcademicWork.objects.filter(type=work_type, status='c', end_date__gt=start_date,
                                                              end_date__lt=end_date).order_by('-end_date')

        # Show all the academic works that are in progress within the selected period
        result_status_in_progress = AcademicWork.objects.filter(type=work_type, status='i',
                                                                start_date__lt=end_date).order_by('-end_date')

        if end_date >= start_date:
            context = {'result_status_concluded': result_status_concluded,
                       'result_status_in_progress': result_status_in_progress, 'type': work_type}
            return render(request, 'report/research/academic_works_report.html', context)
        else:
            messages.error(request, _('End date should be equal or greater than start date.'))
            context = {'types': work_type}
            return render(request, 'report/research/academic_works.html', context)

    context = {'types': types}

    return render(request, 'report/research/academic_works.html', context)