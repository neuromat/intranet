from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from models import AcademicWork, PublishedInPeriodical, Published, Accepted, Submitted, Draft, Periodical, Event
import datetime
from django.template.loader import render_to_string
from django.db.models import Q
from itertools import chain

TIME = " 00:00:00"

def valid_date(date):
    day = date[0:2]
    month = date[3:5]
    if (01 <= int(day) <= 31) and (01 <= int(month) <= 12):
        return True
    else:
        return False

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
            if valid_date(start_date):
                start_date = start_date_typed(start_date)
            else:
                messages.error(request, _('Invalid start date!'))
                return render(request, 'report/research/articles.html')
        else:
            start_date = datetime.datetime.strptime('19700101 00:00:00', '%Y%m%d %H:%M:%S').date()

        end_date = request.POST['end_date']
        if end_date:
            if valid_date(end_date):
                end_date = end_date_typed(end_date)
            else:
                messages.error(request, _('Invalid end date!'))
                return render(request, 'report/research/articles.html')
        else:
            end_date = now_plus_five_years()

        # List of articles
        published_periodical = PublishedInPeriodical.objects.filter(article__type='p', date__gt=start_date,
                                                                    date__lt=end_date).order_by('date')
        published_event = Published.objects.filter(article__type='e', article__event__start_date__lt=end_date,
                                                   article__event__end_date__gt=start_date).order_by('article__event__start_date')
        accepted = Accepted.objects.filter(date__lt=end_date).order_by('date')
        submitted = Submitted.objects.filter(date__lt=end_date).order_by('article_id').distinct('article_id')
        draft = Draft.objects.filter(date__lt=end_date).order_by('article_id').distinct('article_id')

        # Articles IDs
        published_periodical_ids = published_periodical.values_list('article_id', flat=True)
        published_event_ids = published_event.values_list('article_id', flat=True)
        published_ids = list(chain(published_periodical_ids, published_event_ids))
        accepted_ids = accepted.values_list('article_id', flat=True).exclude(article_id__in=published_ids)
        submitted_ids = submitted.values_list('article_id', flat=True).exclude(Q(article_id__in=published_ids) |
                                                                               Q(article_id__in=accepted_ids))
        draft_ids = draft.values_list('article_id', flat=True).exclude(Q(article_id__in=published_ids) |
                                                                       Q(article_id__in=accepted_ids) |
                                                                       Q(article_id__in=submitted_ids))

        # Articles from the scientific team
        published_scientific = published_periodical.filter(article__team='s')
        accepted_scientific = accepted.filter(article__type='p', article__team='s', article_id__in=accepted_ids)
        submitted_scientific = submitted.filter(article__team='s', article_id__in=submitted_ids)
        draft_scientific = draft.filter(article__team='s', article_id__in=draft_ids)

        # Articles from the dissemination team
        published_dissemin = published_periodical.filter(article__team='d')
        accepted_dissemin = accepted.filter(article__type='p', article__team='d', article_id__in=accepted_ids)
        submitted_dissemin = submitted.filter(article__team='d', article_id__in=submitted_ids)
        draft_dissemin = draft.filter(article__team='d', article_id__in=draft_ids)

        # Articles from the technology transfer team
        published_tec_trans = published_periodical.filter(article__team='t')
        accepted_tec_trans = accepted.filter(article__type='p', article__team='t', article_id__in=accepted_ids)
        submitted_tec_trans = submitted.filter(article__team='t', article_id__in=submitted_ids)
        draft_tec_trans = draft.filter(article__team='t', article_id__in=draft_ids)

        # Event articles from the scientific team
        published_scientific_in_event = published_event.filter(article__team='s')
        accepted_scientific_in_event = accepted.filter(article__type='e', article__team='s', article_id__in=accepted_ids)

        # Event articles from the dissemination team
        published_dissemin_in_event = published_event.filter(article__team='d')
        accepted_dissemin_in_event = accepted.filter(article__type='e', article__team='d', article_id__in=accepted_ids)

        # Event articles from the technology transfer team
        published_tec_trans_in_event = published_event.filter(article__team='t')
        accepted_tec_trans_in_event = accepted.filter(article__type='e', article__team='t', article_id__in=accepted_ids)

        if start_date < end_date:
            context = {'published_scientific': published_scientific, 'accepted_scientific': accepted_scientific,
                       'submitted_scientific': submitted_scientific, 'draft_scientific': draft_scientific,
                       'published_dissemin': published_dissemin, 'accepted_dissemin': accepted_dissemin,
                       'submitted_dissemin': submitted_dissemin, 'draft_dissemin': draft_dissemin,
                       'published_tec_trans': published_tec_trans, 'accepted_tec_trans': accepted_tec_trans,
                       'submitted_tec_trans': submitted_tec_trans, 'draft_tec_trans': draft_tec_trans,
                       'published_scientific_in_event': published_scientific_in_event,
                       'accepted_scientific_in_event': accepted_scientific_in_event,
                       'published_dissemin_in_event': published_dissemin_in_event,
                       'accepted_dissemin_in_event': accepted_dissemin_in_event,
                       'published_tec_trans_in_event': published_tec_trans_in_event,
                       'accepted_tec_trans_in_event': accepted_tec_trans_in_event}
            return render(request, 'report/research/articles_report.html', context)
        else:
            messages.error(request, _('End date should be equal or greater than start date.'))
            return render(request, 'report/research/articles.html')

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


@login_required
def import_papers(request):
    if request.method == 'POST':
        if request.FILES:
            file = request.FILES['file'].read().splitlines()
            paper = {}
            papers = []

            # Creating a list of dicts where each dict is a paper.
            for line in file:
                words = line.split()
                if words == []: continue
                elif words[0] == 'ER':
                    papers.append(paper)
                    paper = {}
                else:
                    key = words[0]
                    values = words[2:]
                    values = ' '.join(values)
                    paper[key] = values

            # Look for periodicals. Remove duplicates and arXiv papers.
            periodicals = [key['JO'] for key in papers if 'JO' in key and 'JOUR' in key.values()]
            periodicals = list(set(periodicals))
            periodicals = [name for name in periodicals if not name.startswith('arXiv')]

            periodicals_to_add = []
            for periodical in periodicals:
                if not Periodical.objects.filter(name=periodical):
                    periodicals_to_add.append(periodical)

            # Look for events and remove duplicates
            events_ty_jour = [key['JO'] for key in papers if 'JO' in key and 'CONF' in key.values()]
            events_ty_chap = [key['T2'] for key in papers if 'T2' in key and 'CHAP' in key.values()]
            events = events_ty_jour + events_ty_chap
            events = list(set(events))

            events_to_add = []
            for event in events:
                if not Event.objects.filter(name=event):
                    events_to_add.append(event)

            context = {'periodicals_to_add': periodicals_to_add, 'events_to_add': events_to_add}
            return render(request, 'report/research/papers_to_import.html', context)

    return render(request, 'report/research/import.html')