from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from models import AcademicWork, Published, Unpublished
import datetime
from django.template.loader import render_to_string
from django.db.models import Q
from itertools import chain

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

        published = Published.objects.filter(article__research_result_type='a', date__gt=start_date, date__lt=end_date).values_list('article_id', flat=True)
        accepted = Unpublished.objects.filter(article__research_result_type='a', type='a', date__lt=end_date).values_list('article_id', flat=True)
        submitted = Unpublished.objects.filter(article__research_result_type='a', type='s', date__lt=end_date).values_list('article_id', flat=True)
        accepted_list = list(chain(published, accepted))
        submitted_list = list(chain(published, accepted, submitted))

        # Articles from the scientific team
        published_scientific = Published.objects.filter(article__research_result_type='a', article__team='s',
                                                        date__gt=start_date, date__lt=end_date).order_by('date')

        accepted_scientific = Unpublished.objects.filter(article__research_result_type='a', article__team='s', type='a',
                                                         date__lt=end_date).exclude(article_id__in=published).order_by('date')

        submitted_scientific = Unpublished.objects.filter(article__research_result_type='a', article__team='s', type='s',
                                                          date__lt=end_date).exclude(article_id__in=accepted_list).order_by('date')

        draft_scientific = Unpublished.objects.filter(article__research_result_type='a', article__team='s', type='d',
                                                      date__lt=end_date).exclude(article_id__in=submitted_list).order_by('date')

        # Articles from the dissemination team
        published_dissemin = Published.objects.filter(article__research_result_type='a', article__team='d',
                                                      date__gt=start_date, date__lt=end_date).order_by('date')

        accepted_dissemin = Unpublished.objects.filter(article__research_result_type='a', article__team='d', type='a',
                                                       date__gt=start_date).exclude(article_id__in=published).order_by('date')

        submitted_dissemin = Unpublished.objects.filter(article__research_result_type='a', article__team='d', type='s',
                                                        date__gt=start_date).exclude(article_id__in=accepted_list).order_by('date')

        draft_dissemin = Unpublished.objects.filter(article__research_result_type='a', article__team='d', type='d',
                                                    date__gt=start_date).exclude(article_id__in=submitted_list).order_by('date')

        # Articles from the technology transfer team
        published_tec_trans = Published.objects.filter(article__research_result_type='a', article__team='t',
                                                       date__gt=start_date, date__lt=end_date).order_by('date')

        accepted_tec_trans = Unpublished.objects.filter(article__research_result_type='a', article__team='t', type='a',
                                                        date__gt=start_date).exclude(article_id__in=published).order_by('date')

        submitted_tec_trans = Unpublished.objects.filter(article__research_result_type='a', article__team='t', type='s',
                                                         date__gt=start_date).exclude(article_id__in=accepted_list).order_by('date')

        draft_tec_trans = Unpublished.objects.filter(article__research_result_type='a', article__team='t', type='d',
                                                     date__gt=start_date).exclude(article_id__in=submitted_list).order_by('date')

        if start_date < end_date:
            context = {'published_scientific': published_scientific, 'accepted_scientific': accepted_scientific,
                       'submitted_scientific': submitted_scientific, 'draft_scientific': draft_scientific,
                       'published_dissemin': published_dissemin, 'accepted_dissemin': accepted_dissemin,
                       'submitted_dissemin': submitted_dissemin, 'draft_dissemin': draft_dissemin,
                       'published_tec_trans': published_tec_trans, 'accepted_tec_trans': accepted_tec_trans,
                       'submitted_tec_trans': submitted_tec_trans, 'draft_tec_trans': draft_tec_trans}
            return render(request, 'report/research/articles_report.html', context)

    return render(request, 'report/research/articles.html')


def search_academic_works(start_date, end_date):
    # Get all the Postdocs among the chosen dates
    postdoc_concluded = AcademicWork.objects.filter(type__name='Post-doctoral', end_date__gt=start_date,
                                                    end_date__lt=end_date).order_by('-end_date')
    postdoc_in_progress = AcademicWork.objects.filter(Q(end_date__isnull=True) | Q(end_date__gt=end_date),
                                                      type__name='Post-doctoral',
                                                      start_date__lt=end_date).order_by('-start_date')

    # Get all the PhDs among the chosen dates
    phd_concluded = AcademicWork.objects.filter(type__name='PhD', end_date__gt=start_date,
                                                end_date__lt=end_date).order_by('-end_date')
    phd_in_progress = AcademicWork.objects.filter(Q(end_date__isnull=True) | Q(end_date__gt=end_date),
                                                  type__name='PhD', start_date__lt=end_date).order_by('-start_date')

    # Get all the MScs among the chosen dates
    msc_concluded = AcademicWork.objects.filter(type__name='MSc', end_date__gt=start_date,
                                                end_date__lt=end_date).order_by('-end_date')
    msc_in_progress = AcademicWork.objects.filter(Q(end_date__isnull=True) | Q(end_date__gt=end_date),
                                                  type__name='MSc', start_date__lt=end_date).order_by('-start_date')

    return postdoc_concluded, postdoc_in_progress, phd_concluded, phd_in_progress, msc_concluded, msc_in_progress


@login_required
def academic_works(request):
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

        postdoc_concluded, postdoc_in_progress, phd_concluded, phd_in_progress, msc_concluded, msc_in_progress = search_academic_works(start_date, end_date)

        if end_date >= start_date:
            context = {'postdoc_concluded': postdoc_concluded, 'postdoc_in_progress': postdoc_in_progress,
                       'phd_concluded': phd_concluded, 'phd_in_progress': phd_in_progress,
                       'msc_concluded': msc_concluded, 'msc_in_progress': msc_in_progress,
                       'start_date': start_date, 'end_date': end_date}

            return render(request, 'report/research/academic_works_report.html', context)
        else:
            messages.error(request, _('End date should be equal or greater than start date.'))
            return render(request, 'report/research/academic_works.html')

    return render(request, 'report/research/academic_works.html')


@login_required
def academic_works_tex(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    postdoc_concluded, postdoc_in_progress, phd_concluded, phd_in_progress, msc_concluded, msc_in_progress = search_academic_works(start_date, end_date)

    context = {'postdoc_concluded': postdoc_concluded, 'postdoc_in_progress': postdoc_in_progress,
               'phd_concluded': phd_concluded, 'phd_in_progress': phd_in_progress,
               'msc_concluded': msc_concluded, 'msc_in_progress': msc_in_progress}

    response = HttpResponse(render_to_string('report/research/tex/academic_works.tex', context), content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="academic_works.tex"'
    return response