# -*- coding: utf-8 -*-
import datetime
import urllib2
import HTMLParser
import re
import time
from itertools import chain
from random import randint
from bs4 import BeautifulSoup
from research.models import *
from person.models import CitationName
from helper_functions.latex import tex_escape
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import render, HttpResponse, redirect
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _


TIME = " 00:00:00"
SCHOLAR = 'https://scholar.google.com.br'
SCHOLAR_USER = '/citations?user=OaY57UIAAAAJ&cstart=00&pagesize=1000'


def valid_date(date):
    day = date[0:2]
    month = date[3:5]
    year = date[6:]
    return (01 <= int(day) <= 31) and (01 <= int(month) <= 12) and (int(year) >= 0)


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


def search_articles(start_date, end_date):
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

    return published_scientific, accepted_scientific, submitted_scientific, draft_scientific, published_dissemin, \
        accepted_dissemin, submitted_dissemin, draft_dissemin, published_tec_trans, accepted_tec_trans, \
        submitted_tec_trans, draft_tec_trans, published_scientific_in_event, accepted_scientific_in_event, \
        published_dissemin_in_event, accepted_dissemin_in_event, published_tec_trans_in_event, \
        accepted_tec_trans_in_event


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

        published_scientific, accepted_scientific, submitted_scientific, draft_scientific, published_dissemin, \
            accepted_dissemin, submitted_dissemin, draft_dissemin, published_tec_trans, accepted_tec_trans, \
            submitted_tec_trans, draft_tec_trans, published_scientific_in_event, accepted_scientific_in_event, \
            published_dissemin_in_event, accepted_dissemin_in_event, published_tec_trans_in_event, \
            accepted_tec_trans_in_event = search_articles(start_date, end_date)

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
                       'accepted_tec_trans_in_event': accepted_tec_trans_in_event,
                       'start_date': start_date, 'end_date': end_date}
            return render(request, 'report/research/articles_report.html', context)
        else:
            messages.error(request, _('End date should be equal or greater than start date.'))
            return render(request, 'report/research/articles.html')

    return render(request, 'report/research/articles.html')


@login_required
def articles_tex(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    published_scientific, accepted_scientific, submitted_scientific, draft_scientific, published_dissemin, \
        accepted_dissemin, submitted_dissemin, draft_dissemin, published_tec_trans, accepted_tec_trans, \
        submitted_tec_trans, draft_tec_trans, published_scientific_in_event, accepted_scientific_in_event, \
        published_dissemin_in_event, accepted_dissemin_in_event, published_tec_trans_in_event, \
        accepted_tec_trans_in_event = search_articles(start_date, end_date)

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

    response = render_to_string('report/research/tex/articles.tex', context)
    response = tex_escape(response)
    latex_response = HttpResponse(response, content_type='text/plain')
    latex_response['Content-Disposition'] = 'attachment; filename="articles.tex"'

    return latex_response


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

        postdoc_concluded, postdoc_in_progress, phd_concluded, phd_in_progress, msc_concluded, \
            msc_in_progress = search_academic_works(start_date, end_date)

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

    postdoc_concluded, postdoc_in_progress, phd_concluded, phd_in_progress, msc_concluded, \
        msc_in_progress = search_academic_works(start_date, end_date)

    context = {'postdoc_concluded': postdoc_concluded, 'postdoc_in_progress': postdoc_in_progress,
               'phd_concluded': phd_concluded, 'phd_in_progress': phd_in_progress,
               'msc_concluded': msc_concluded, 'msc_in_progress': msc_in_progress}

    response = HttpResponse(render_to_string('report/research/tex/academic_works.tex', context),
                            content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="academic_works.tex"'
    return response


def scholar():
    """

    This method gets all articles on Neuromat's google scholar account

    """

    html_scholar = urllib2.urlopen(SCHOLAR+SCHOLAR_USER).read()
    soup = BeautifulSoup(html_scholar)

    scholar_list = []
    for line in soup.find_all('a'):
        line = str(line)
        if 'class="gsc_a_at"' in line:
            try:
                link = re.search('href="(.+?)">', line).group(1)
                title = re.search('">(.+?)</a>', line).group(1)
            except AttributeError:
                link = ''
                title = ''
            if link != '' and title != '':
                paper = {title: link}
                scholar_list.append(paper)

    return scholar_list


def scholar_info(scholar_list, paper_title):
    """
    From Neuromat's google scholar, this method retrieves the date and link of a specific paper, returning a tuple

    """
    paper_url = ''
    for each_dict in scholar_list:
        for each_key in each_dict:
            if paper_title in each_key:
                paper_url = each_dict[each_key]

    html_parser = HTMLParser.HTMLParser()
    citation_link = html_parser.unescape(paper_url)

    html_paper = urllib2.urlopen(SCHOLAR+citation_link).read()
    soup = BeautifulSoup(html_paper)

    date = ''
    for line in soup:
        line = str(line)
        try:
            date = re.search('<div class="gsc_field">Data de publicação</div><div class="gsc_value">(.+?)</div>',
                             line).group(1)
        except AttributeError:
            date = ''

    if date != '':
        date_format = date.split('/')
        if len(date_format) == 3:
            date = datetime.datetime.strptime(date, '%Y/%m/%d').date()

    gsc_class = str(soup.find(class_=re.compile("gsc_title_link")))
    url = re.search('href="(.+?)"', gsc_class).group(1)

    return date, url


def arxiv(arxiv_url):
    html = urllib2.urlopen(arxiv_url).read()
    soup = BeautifulSoup(html)
    line = soup.find_all("div", class_="dateline")
    line = str(line[0])

    if 'last revised' in line:
        try:
            date = re.search(' last revised (.+?) \(this version', line).group(1)
        except AttributeError:
            date = ''
    else:
        try:
            date = re.search('Submitted on (.+?)\)</div>', line).group(1)
        except AttributeError:
            date = ''

    if date != '':
        date = datetime.datetime.strptime(date, '%d %b %Y').date()

    return date


@login_required
def import_papers(request):
    """
    This method imports papers from a RIS file and stores them on cache.

    """

    if request.method == 'POST':
        if request.FILES and request.FILES['file'].name.endswith('.ris'):
            file_uploaded = request.FILES['file'].read().splitlines()
            paper = {}
            papers = []
            list_a1 = []

            # Creating a list of dicts where each dict is a paper.
            for line in file_uploaded:
                words = line.split()
                if words == []:
                    continue
                elif words[0] == 'ER':
                    paper['A1'] = list_a1
                    papers.append(paper)
                    paper = {}
                    list_a1 = []
                elif words[0] == 'A1':
                    values = words[2:]
                    values = ' '.join(values)
                    list_a1.append(values)
                else:
                    key = words[0]
                    values = words[2:]
                    values = ' '.join(values)
                    paper[key] = values

            # Look for periodical to be registered. Remove duplicates and arXiv papers.
            periodicals = [key['JO'] for key in papers if 'JO' in key and 'JOUR' in key.values()]
            periodicals = list(set(periodicals))
            periodicals = [name for name in periodicals if not name.startswith('arXiv')]

            periodicals_to_add = []
            for periodical in periodicals:
                if not Periodical.objects.filter(name=periodical) \
                        and not PeriodicalRISFile.objects.filter(name=periodical):
                    periodicals_to_add.append(periodical)

            # Cache the list of papers and the list of periodicals to add
            cache.set('papers', papers, 60 * 30)
            cache.set('periodicals_to_add', periodicals_to_add, 60 * 30)

            context = {'periodicals_to_add': periodicals_to_add}
            return render(request, 'report/research/periodicals_to_import.html', context)

        else:
            messages.warning(request, _("Please, select a .ris file to upload."))

    return render(request, 'report/research/import.html')


def add_periodicals(request):

    """

    This method adds periodicals to NIRA's database using date obtained from Google Scholar

    """

    if request.method == "POST":

        # Add the journals selected by the user
        if request.POST['action'] == "add":
            periodicals = request.POST.getlist('periodicals_to_add')
            periodicals_to_add = cache.get('periodicals_to_add')

            if periodicals:
                num_of_periodicals = len(periodicals)
                for periodical in periodicals:
                    name = Periodical(name=periodical)
                    name.save()
                    periodicals_to_add.remove(periodical)

                if num_of_periodicals == 1:
                    messages.success(request, _('Successfully added one Periodical.'))
                else:
                    messages.success(request, _('Successfully added all the Periodicals.'))

            else:
                messages.warning(request, _('You have selected no item. Nothing to be done!'))

            cache.set('periodicals_to_add', periodicals_to_add, 60 * 30)
            context = {'periodicals_to_add': periodicals_to_add}
            return render(request, 'report/research/periodicals_to_import.html', context)

        # Go to the page that shows the events, with cache properly set
        elif request.POST['action'] == "next":
            papers = cache.get('papers')
            # Look for event to be registered. Remove duplicates
            events_ty_jour = [key['JO'] for key in papers if 'JO' in key and 'CONF' in key.values()]
            events_ty_chap = [key['T2'] for key in papers if 'T2' in key and 'CHAP' in key.values()]
            events = events_ty_jour + events_ty_chap
            events = list(set(events))

            # Events that need to be added
            events_to_add = []
            for event in events:
                if not Event.objects.filter(name=event) and not EventRISFile.objects.filter(name=event):
                    events_to_add.append(event)

            cache.set('events', events_to_add, 60 * 30)
            context = {'events_to_add': events_to_add}
            return render(request, 'report/research/events_to_import.html', context)

        # Back to the initial page
        elif request.POST['action'] == "back":
            cache.delete_many(['papers', 'periodicals_to_add', 'events'])
            return redirect('import_papers')

    return redirect('import_papers')


def add_papers(request):
    """
    Adding papers to NIRA's database using date obtained from Google Scholar
    """

    # If user wants to add papers
    if request.method == "POST":

        # Do the list of papers to add
        if request.POST['action'] == "next":

            # If already is in cache, do not make a new search
            if cache.get('periodical_published_papers'):
                periodical_published_papers = cache.get('periodical_published_papers')
                periodicals = Periodical.objects.all()
                context = {'periodical_published_papers': periodical_published_papers, 'periodicals': periodicals}
                # If you have the published papers, go to the next step
                return render(request, 'report/research/periodical_published_papers.html', context)

            # Let's read the papers
            else:
                citations = CitationName.objects.all()
                papers = cache.get('papers')
                periodical_published_papers = []
                arxiv_papers = []
                event_papers = []
                periodical_update_papers = []
                scholar_list = scholar()
                periodicals = Periodical.objects.all()
                periodical_ris_file = PeriodicalRISFile.objects.all()
                events = Event.objects.all()
                events_ris_file = EventRISFile.objects.all()
                paper_scholar_id = 0
                paper_arxiv_id = 0

                # For each paper...
                for each_dict in papers:
                    paper_type = ''
                    paper_title = ''
                    paper_author = ''
                    paper_journal = ''
                    periodical_id = ''
                    event_id = ''
                    paper_volume = ''
                    paper_issue = ''
                    paper_start_page = ''
                    paper_end_page = ''
                    registered_title = False
                    get_paper_status = ''
                    get_paper_team = ''
                    nira_author_list = []

                    for each_key in each_dict:

                        # Paper type
                        if 'TY' in each_key:
                            paper_type = each_dict[each_key]

                        # Paper title
                        elif 'T1' in each_key:
                            paper_title = each_dict[each_key]
                            if paper_title.isupper():
                                paper_title = paper_title.capitalize()
                            if ResearchResult.objects.filter(title=paper_title):
                                registered_title = True
                                get_paper = Article.objects.get(title=paper_title)
                                get_paper_status = get_paper.status
                                get_paper_team = get_paper.team

                        # Paper authors and citation names
                        elif 'A1' in each_key:
                            paper_author = each_dict[each_key]
                            citation_names = ''
                            for author in paper_author:
                                if author.isupper():
                                    author = author.title()
                                names = author.split(',')
                                last_name = names[0]
                                other_names = names[1]
                                names = other_names.split()
                                invalid_name = ['e', 'da', 'do', 'de', 'dos', 'E', 'Da', 'Do', 'De', 'Dos']
                                letters = ''
                                for name in names:
                                    if name not in invalid_name:
                                        letters += name[0]

                                if author.lower() == paper_author[-1].lower():
                                    citation_name = last_name+','+' '+letters+'.'
                                else:
                                    citation_name = last_name+','+' '+letters+';'+' '

                                if citations.filter(name=last_name+','+' '+letters):
                                    nira_author_name = citations.get(name=last_name+','+' '+letters)
                                    nira_author_name = nira_author_name.person
                                    nira_author_list.append(nira_author_name)

                                citation_names += citation_name

                            paper_author = citation_names

                        # Journal of publication
                        elif 'JO' in each_key:
                            paper_journal = each_dict[each_key]
                            if not paper_journal.startswith('arXiv'):
                                if periodicals.filter(name=paper_journal):
                                    get_periodical = periodicals.get(name=paper_journal)
                                    periodical_id = get_periodical.pk
                                elif periodicals.filter(acronym=paper_journal):
                                    get_periodical = periodicals.get(acronym=paper_journal)
                                    periodical_id = get_periodical.pk
                                elif periodical_ris_file.filter(name=paper_journal):
                                    get_periodical = periodical_ris_file.get(name=paper_journal)
                                    periodical_id = get_periodical.periodical_id
                                elif events.filter(name=paper_journal):
                                    get_event = events.get(name=paper_journal)
                                    event_id = get_event.pk
                                elif events_ris_file.filter(name=paper_journal):
                                    get_event = events_ris_file.get(name=paper_journal)
                                    event_id = get_event.event_id
                                else:
                                    periodical_id = ''
                                    event_id = ''

                        # Event of paper
                        elif 'T2' in each_key:
                            paper_event = each_dict[each_key]
                            if events.filter(name=paper_event):
                                get_event = events.get(name=paper_event)
                                event_id = get_event.pk
                            elif events_ris_file.filter(name=paper_event):
                                get_event = events_ris_file.get(name=paper_event)
                                event_id = get_event.event_id
                            else:
                                event_id = ''

                        # Volume of paper publication
                        elif 'VL' in each_key:
                            paper_volume = each_dict[each_key]

                        # Issue of paper publication
                        elif 'IS' in each_key:
                            paper_issue = each_dict[each_key]

                        # Starting page of paper in publication
                        elif 'SP' in each_key:
                            paper_start_page = each_dict[each_key]

                        # Last page of paper in publication
                        elif 'EP' in each_key:
                            paper_end_page = each_dict[each_key]

                    if nira_author_list:
                        paper = {'nira_author_list': nira_author_list, 'paper_title': paper_title,
                                 'paper_author': paper_author}
                    else:
                        paper = {'paper_title': paper_title, 'paper_author': paper_author}

                    # If the paper wasn't published before, get the date of publication using Google Scholar
                    if registered_title:
                        if u'p' not in get_paper_status and not paper_journal.startswith('arXiv'):
                            paper['paper_team'] = get_paper_team
                            paper['paper_volume'] = paper_volume
                            paper['paper_issue'] = paper_issue
                            paper['paper_start_page'] = paper_start_page
                            paper['paper_end_page'] = paper_end_page
                            paper['paper_scholar_id'] = paper_scholar_id
                            paper_scholar_id += 1
                            paper_info = scholar_info(scholar_list, paper_title)
                            paper_date = paper_info[0]
                            paper_url = paper_info[1]
                            paper['periodical_id'] = periodical_id
                            paper['paper_date'] = paper_date
                            paper['url'] = paper_url
                            periodical_update_papers.append(paper)

                            # Wait 2 to 5 seconds to do the next paper.
                            time.sleep(randint(2, 5))

                    else:
                        if 'JOUR' in paper_type:
                            if paper_journal.startswith('arXiv'):
                                paper['paper_arxiv_id'] = paper_arxiv_id
                                paper_arxiv_id += 1
                                arxiv_txt = paper_journal.split(':')
                                arxiv_url = 'http://arxiv.org/abs/'+str(arxiv_txt[1])
                                paper_date = arxiv(arxiv_url)
                                paper['arxiv_url'] = arxiv_url
                                paper['paper_date'] = paper_date
                                arxiv_papers.append(paper)
                            else:
                                paper['paper_volume'] = paper_volume
                                paper['paper_issue'] = paper_issue
                                paper['paper_start_page'] = paper_start_page
                                paper['paper_end_page'] = paper_end_page
                                paper['paper_scholar_id'] = paper_scholar_id
                                paper_scholar_id += 1
                                paper_info = scholar_info(scholar_list, paper_title)
                                paper_date = paper_info[0]
                                paper_url = paper_info[1]
                                paper['periodical_id'] = periodical_id
                                paper['paper_date'] = paper_date
                                paper['url'] = paper_url
                                periodical_published_papers.append(paper)

                            # Wait 2 to 5 seconds to do the next paper.
                            time.sleep(randint(2, 5))

                        elif 'CONF' in paper_type:
                            paper['paper_start_page'] = paper_start_page
                            paper['paper_end_page'] = paper_end_page
                            paper['paper_scholar_id'] = paper_scholar_id
                            paper_scholar_id += 1
                            paper['event_id'] = event_id
                            event_papers.append(paper)

                cache.set('periodical_published_papers', periodical_published_papers, 60 * 30)
                cache.set('arxiv_papers', arxiv_papers, 60 * 30)
                cache.set('periodical_update_papers', periodical_update_papers, 60 * 30)
                cache.set('event_papers', event_papers, 60 * 30)

                context = {'periodical_published_papers': periodical_published_papers, 'periodicals': periodicals}
                return render(request, 'report/research/periodical_published_papers.html', context)

        # Back to the list of periodicals to add
        elif request.POST['action'] == "back":
            periodicals_to_add = cache.get('periodicals_to_add')
            context = {'periodicals_to_add': periodicals_to_add}
            return render(request, 'report/research/periodicals_to_import.html', context)

    return redirect('import_papers')


def periodical_published_papers(request):
    if request.method == "POST":
        # Add published papers
        if request.POST['action'] == "add":
            selected_papers = request.POST.getlist('paper_id')
            periodical_published_papers = cache.get('periodical_published_papers')
            periodicals = Periodical.objects.all()

            if selected_papers:
                date_error = False

                for paper_scholar_id in selected_papers:

                    paper_author = []
                    paper_url = ''

                    for paper in periodical_published_papers:
                        if paper['paper_scholar_id'] == int(paper_scholar_id):
                            paper_url = paper['url']
                            try:
                                paper_author = paper['nira_author_list']
                            except KeyError:
                                pass

                    paper_team = request.POST['paper_team_'+paper_scholar_id]
                    paper_title = request.POST['paper_title_'+paper_scholar_id]
                    paper_ris_author = request.POST['paper_author_'+paper_scholar_id]
                    paper_periodical = request.POST['paper_periodical_'+paper_scholar_id]
                    paper_volume = request.POST['paper_volume_'+paper_scholar_id]
                    paper_issue = request.POST['paper_issue_'+paper_scholar_id]
                    paper_start_page = request.POST['paper_start_page_'+paper_scholar_id]
                    paper_end_page = request.POST['paper_end_page_'+paper_scholar_id]
                    paper_date = request.POST['paper_date_'+paper_scholar_id]

                    # Date field validation
                    paper_date_error = False
                    try:
                        datetime.datetime.strptime(paper_date, '%Y-%m-%d')
                    except ValueError:
                        paper_date_error = True
                        date_error = True

                    if not paper_date_error:
                        # Adding paper in NIRA
                        periodical = Periodical.objects.get(id=int(paper_periodical))
                        article = Article(team=paper_team, title=paper_title, ris_file_authors=paper_ris_author,
                                          status='p', type='p', periodical=periodical, url=paper_url)
                        article.save()
                        article_id = article.pk
                        # start_page and end_page are integers, so they can't be blank
                        if paper_start_page and paper_end_page:
                            published = PublishedInPeriodical(article_id=article_id, volume=paper_volume,
                                                              number=paper_issue, date=paper_date,
                                                              start_page=paper_start_page, end_page=paper_end_page)
                            published.save()

                            if paper_author:
                                for author in range(0, len(paper_author)):
                                    person_id = paper_author[author].pk
                                    Author(research_result_id=article_id, author_id=person_id, order=author+1).save()

                        else:
                            published = PublishedInPeriodical(article_id=article_id, volume=paper_volume,
                                                              number=paper_issue, date=paper_date)
                            published.save()

                            if paper_author:
                                for author in range(0, len(paper_author)):
                                    person_id = paper_author[author].pk
                                    Author(research_result_id=article_id, author_id=person_id, order=author+1).save()

                        # Removing paper from the periodical_published_papers list
                        periodical_published_papers = [x for x in periodical_published_papers if
                                                       not (int(paper_scholar_id) == x.get('paper_scholar_id'))]

                if date_error:
                    messages.warning(request, _('Wrong date format! It should be YYYY-MM-DD.'))

                cache.set('periodical_published_papers', periodical_published_papers, 60 * 30)
                context = {'periodical_published_papers': periodical_published_papers, 'periodicals': periodicals}
                return render(request, 'report/research/periodical_published_papers.html', context)

            else:
                messages.warning(request, _('You have selected no item. Nothing to be done!'))
                context = {'periodical_published_papers': periodical_published_papers, 'periodicals': periodicals}
                return render(request, 'report/research/periodical_published_papers.html', context)

        # Go to the page that shows the arxiv papers to add
        elif request.POST['action'] == "next":
            arxiv_papers = cache.get('arxiv_papers')
            context = {'arxiv_papers': arxiv_papers}
            return render(request, 'report/research/arxiv_papers.html', context)

        # Back to the list of events to add
        elif request.POST['action'] == "back":
            events_to_add = cache.get('events')
            context = {'events_to_add': events_to_add}
            return render(request, 'report/research/events_to_import.html', context)

    return redirect('import_papers')


def arxiv_papers(request):
    if request.method == "POST":
        # Add arxiv papers
        if request.POST['action'] == "add":
            arxiv_papers = cache.get('arxiv_papers')
            selected_papers = request.POST.getlist('paper_id')
            if selected_papers:

                date_error = False

                for paper_arxiv_id in selected_papers:

                    paper_x_author = []

                    for paper in arxiv_papers:
                        if paper['paper_arxiv_id'] == int(paper_arxiv_id):
                            try:
                                paper_x_author = paper['nira_author_list']
                            except KeyError:
                                pass

                    paper_team = request.POST['paper_team_'+paper_arxiv_id]
                    paper_title = request.POST['paper_title_'+paper_arxiv_id]
                    paper_author = request.POST['paper_author_'+paper_arxiv_id]
                    arxiv_url = request.POST['paper_arxiv_'+paper_arxiv_id]
                    paper_date = request.POST['paper_date_'+paper_arxiv_id]

                    # Date field validation
                    paper_date_error = False
                    try:
                        datetime.datetime.strptime(paper_date, '%Y-%m-%d')
                    except ValueError:
                        paper_date_error = True
                        date_error = True

                    if not paper_date_error:
                        # Adding paper in NIRA
                        item = Article(team=paper_team, title=paper_title, ris_file_authors=paper_author, url=arxiv_url,
                                       status='d')
                        item.save()
                        article_id = item.pk
                        date = Draft(article_id=article_id, date=paper_date)
                        date.save()

                        if paper_x_author:
                            for author in range(0, len(paper_x_author)):
                                person_id = paper_x_author[author].pk
                                Author(research_result_id=article_id, author_id=person_id, order=author+1).save()

                        # Removing paper from the arxiv_papers list
                        arxiv_papers = [x for x in arxiv_papers if not (int(paper_arxiv_id) == x.get('paper_arxiv_id'))]

                if date_error:
                    messages.warning(request, _('Wrong date format! It should be YYYY-MM-DD.'))

                cache.set('arxiv_papers', arxiv_papers, 60 * 30)
                context = {'arxiv_papers': arxiv_papers}
                return render(request, 'report/research/arxiv_papers.html', context)

            else:
                messages.warning(request, _('You have selected no item. Nothing to be done!'))
                context = {'arxiv_papers': arxiv_papers}
                return render(request, 'report/research/arxiv_papers.html', context)

        # Go to the page that shows papers from events to add
        elif request.POST['action'] == "next":
            event_papers = cache.get('event_papers')
            events = Event.objects.all()
            context = {'event_papers': event_papers, 'events': events}
            return render(request, 'report/research/add_event_papers.html', context)

        # Back to the list of published papers to add
        elif request.POST['action'] == "back":
            periodical_published_papers = cache.get('periodical_published_papers')
            periodicals = Periodical.objects.all()
            context = {'periodical_published_papers': periodical_published_papers, 'periodicals': periodicals}
            return render(request, 'report/research/periodical_published_papers.html', context)

    return redirect('import_papers')


def event_papers(request):
    if request.method == "POST":
        # Add event papers
        if request.POST['action'] == "add":
            event_papers = cache.get('event_papers')
            selected_papers = request.POST.getlist('paper_id')
            events = Event.objects.all()
            if selected_papers:
                for paper_scholar_id in selected_papers:

                    paper_event_author = []

                    for paper in event_papers:
                        if paper['paper_scholar_id'] == int(paper_scholar_id):
                            try:
                                paper_event_author = paper['nira_author_list']
                            except KeyError:
                                pass

                    paper_team = request.POST['paper_team_'+paper_scholar_id]
                    paper_title = request.POST['paper_title_'+paper_scholar_id]
                    paper_author = request.POST['paper_author_'+paper_scholar_id]
                    paper_event = request.POST['paper_event_'+paper_scholar_id]
                    paper_start_page = request.POST['paper_start_page_'+paper_scholar_id]
                    paper_end_page = request.POST['paper_end_page_'+paper_scholar_id]

                    # Adding paper in NIRA
                    event = Event.objects.get(id=int(paper_event))
                    article = Article(team=paper_team, title=paper_title, ris_file_authors=paper_author, status='p',
                                      type='e', event=event)
                    article.save()
                    article_id = article.pk
                    # start_page and end_page are integers, so they can't be blank
                    if paper_start_page and paper_end_page:
                        published = Published(article_id=article_id, start_page=paper_start_page,
                                              end_page=paper_end_page)
                        published.save()

                        if paper_event_author:
                            for author in range(0, len(paper_event_author)):
                                person_id = paper_event_author[author].pk
                                Author(research_result_id=article_id, author_id=person_id, order=author+1).save()

                    else:
                        published = Published(article_id=article_id)
                        published.save()

                        if paper_event_author:
                            for author in range(0, len(paper_event_author)):
                                person_id = paper_event_author[author].pk
                                Author(research_result_id=article_id, author_id=person_id, order=author+1).save()


                    # Removing paper from the event_papers list
                    event_papers = [x for x in event_papers if not (int(paper_scholar_id) == x.get('paper_scholar_id'))]

                cache.set('event_papers', event_papers, 60 * 30)
                context = {'event_papers': event_papers, 'events': events}
                return render(request, 'report/research/add_event_papers.html', context)

            else:
                messages.warning(request, _('You have selected no item. Nothing to be done!'))
                context = {'event_papers': event_papers, 'events': events}
                return render(request, 'report/research/add_event_papers.html', context)

        # Back to the list of arxiv papers to add
        elif request.POST['action'] == "back":
            arxiv_papers = cache.get('arxiv_papers')
            context = {'arxiv_papers': arxiv_papers}
            return render(request, 'report/research/arxiv_papers.html', context)

        # Go to the page that shows the papers to update
        elif request.POST['action'] == "next":
            periodical_update_papers = cache.get('periodical_update_papers')
            periodicals = Periodical.objects.all()
            context = {'periodical_update_papers': periodical_update_papers, 'periodicals': periodicals}
            return render(request, 'report/research/periodical_update_papers.html', context)

    return redirect('import_papers')


def update_papers(request):
    if request.method == "POST":
        # Update papers
        if request.POST['action'] == "update":
            authors = Author.objects.all()
            selected_papers = request.POST.getlist('paper_id')
            periodical_update_papers = cache.get('periodical_update_papers')
            periodicals = Periodical.objects.all()

            if selected_papers:

                date_error = False

                for paper_scholar_id in selected_papers:

                    paper_update_author = []

                    for paper in periodical_update_papers:
                        if paper['paper_scholar_id'] == int(paper_scholar_id):
                            try:
                                paper_update_author = paper['nira_author_list']
                            except KeyError:
                                pass

                    paper_team = request.POST['paper_team_'+paper_scholar_id]
                    paper_title = request.POST['paper_title_'+paper_scholar_id]
                    paper_author = request.POST['paper_author_'+paper_scholar_id]
                    paper_periodical = request.POST['paper_periodical_'+paper_scholar_id]
                    paper_volume = request.POST['paper_volume_'+paper_scholar_id]
                    paper_issue = request.POST['paper_issue_'+paper_scholar_id]
                    paper_start_page = request.POST['paper_start_page_'+paper_scholar_id]
                    paper_end_page = request.POST['paper_end_page_'+paper_scholar_id]
                    paper_date = request.POST['paper_date_'+paper_scholar_id]

                    # Get ID, URL and staus info
                    paper = Article.objects.get(title=paper_title)
                    paper_id = paper.pk
                    paper_url = paper.url
                    paper_status = paper.status

                    # Date field validation
                    paper_date_error = False
                    try:
                        datetime.datetime.strptime(paper_date, '%Y-%m-%d')
                    except ValueError:
                        paper_date_error = True
                        date_error = True

                    if not paper_date_error:
                        # Updating paper in NIRA
                        periodical = Periodical.objects.get(id=int(paper_periodical))
                        paper_status = re.findall("\\'(.+?)\\'", paper_status)
                        paper_status.append(u'p')
                        article = Article(researchresult_ptr_id=paper_id, team=paper_team, title=paper_title,
                                          ris_file_authors=paper_author, url=paper_url, status=paper_status, type='p',
                                          periodical=periodical)
                        article.save()
                        article_id = article.pk

                        if paper_update_author:

                            if authors.filter(research_result_id=article_id):
                                authors.filter(research_result_id=article_id).delete()

                            for author in range(0, len(paper_update_author)):
                                person_id = paper_update_author[author].pk
                                Author(research_result_id=article_id, author_id=person_id, order=author+1).save()

                        # start_page and end_page are integers, so they can't be blank
                        if paper_start_page and paper_end_page:
                            x = PublishedInPeriodical.objects.all()
                            published = PublishedInPeriodical(article_id=paper_id, volume=paper_volume,
                                                              number=paper_issue, date=paper_date,
                                                              start_page=paper_start_page, end_page=paper_end_page)
                            published.save()
                        else:
                            published = PublishedInPeriodical(article_id=paper_id, volume=paper_volume,
                                                              number=paper_issue, date=paper_date)
                            published.save()

                        # Removing paper from the periodical_published_papers list
                        periodical_update_papers = [x for x in periodical_update_papers if
                                                    not (int(paper_scholar_id) == x.get('paper_scholar_id'))]

                if date_error:
                    messages.warning(request, _('Wrong date format! It should be YYYY-MM-DD.'))

                cache.set('periodical_update_papers', periodical_update_papers, 60 * 30)
                context = {'periodical_update_papers': periodical_update_papers, 'periodicals': periodicals}
                return render(request, 'report/research/periodical_update_papers.html', context)

            else:
                messages.warning(request, _('You have selected no item. Nothing to be done!'))
                context = {'periodical_update_papers': periodical_update_papers, 'periodicals': periodicals}
                return render(request, 'report/research/periodical_update_papers.html', context)

        # Back to the list of event papers to add
        elif request.POST['action'] == "back":
            event_papers = cache.get('event_papers')
            events = Event.objects.all()
            context = {'event_papers': event_papers, 'events': events}
            return render(request, 'report/research/add_event_papers.html', context)

        # Clean the cache. Back to the initial page
        elif request.POST['action'] == "finish":
            cache.delete_many(['papers', 'periodicals_to_add', 'events', 'event_papers', 'arxiv_papers',
                               'periodical_published_papers', 'periodical_update_papers'])
            return redirect('import_papers')

    return redirect('import_papers')
