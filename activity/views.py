from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from activity.models import ProjectActivities, SeminarType
import datetime
from django.contrib import messages

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


@login_required
def seminars_report(request):

    categories = SeminarType.objects.all()

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
            now_plus_30 = datetime.datetime.now() + datetime.timedelta(days=30)
            now_plus_30 = now_plus_30.strftime("%Y%m%d %H:%M:%S")
            end_date = datetime.datetime.strptime(now_plus_30, '%Y%m%d %H:%M:%S').date()

        category = request.POST['category']

        seminars = ProjectActivities.objects.filter(type_of_activity='s', seminar__category=category,
                                                    seminar__date__gt=start_date, seminar__date__lt=end_date)

        if end_date >= start_date:
            context = {'seminars': seminars}
            return render(request, 'report/seminars_report.html', context)
        else:
            messages.error(request, 'End date should be equal or greater than start date.')
            return render(request, 'report/seminars.html')

    context = {'categories': categories}

    return render(request, 'report/seminars.html', context)


@login_required
def training_programs_report(request):

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
            now_plus_30 = datetime.datetime.now() + datetime.timedelta(days=30)
            now_plus_30 = now_plus_30.strftime("%Y%m%d %H:%M:%S")
            end_date = datetime.datetime.strptime(now_plus_30, '%Y%m%d %H:%M:%S').date()

        training_programs = ProjectActivities.objects.filter(type_of_activity='t',
                                                             trainingprogram__start_date__gt=start_date,
                                                             trainingprogram__start_date__lt=end_date)

        if end_date >= start_date:
            context = {'training_programs': training_programs}
            return render(request, 'report/training_programs_report.html', context)
        else:
            messages.error(request, 'End date should be equal or greater than start date.')
            return render(request, 'report/training_programs.html')

    return render(request, 'report/training_programs.html')


@login_required
def meetings_report(request):

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
            now_plus_30 = datetime.datetime.now() + datetime.timedelta(days=30)
            now_plus_30 = now_plus_30.strftime("%Y%m%d %H:%M:%S")
            end_date = datetime.datetime.strptime(now_plus_30, '%Y%m%d %H:%M:%S').date()

        meetings = ProjectActivities.objects.filter(type_of_activity='m', meeting__start_date__gt=start_date,
                                                    meeting__start_date__lt=end_date)

        if end_date >= start_date:
            context = {'meetings': meetings}
            return render(request, 'report/meetings_report.html', context)
        else:
            messages.error(request, 'End date should be equal or greater than start date.')
            return render(request, 'report/meetings.html')

    return render(request, 'report/meetings.html')