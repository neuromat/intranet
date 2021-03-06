from django.db import models
from django.utils.translation import ugettext_lazy as _
from person.models import Person, Institution, CitationName


# Defining types of research results
ARTICLE = 'a'
BOOK_OR_CHAPTER = 'b'
TYPE = (
    (ARTICLE, _('Article')),
    (BOOK_OR_CHAPTER, _('Book')),
)

# Teams
SCIENTIFIC = 's'
DISSEMINATION = 'd'
TECHNOLOGY_TRANSFER = 't'
TEAMS = (
    (SCIENTIFIC, _('Scientific')),
    (DISSEMINATION, _('Dissemination')),
    (TECHNOLOGY_TRANSFER, _('Technology transfer'))
)

# Book or chapter
BOOK = 'b'
CHAPTER = 'c'
TYPE_BOOK_OR_CHAPTER = (
    (BOOK, _('Book')),
    (CHAPTER, _('Chapter')),
)

# Published in a journal or in a conference?
PERIODICAL = 'p'
EVENT = 'e'
ARTICLE_TYPE = (
    (PERIODICAL, _('Periodical (Journal or magazine)')),
    (EVENT, _('Event (Conference, congress, meeting, etc)')),
)

FUNDING_CHOICES = ((True, 'Yes'), (False, 'No'))


class ResearchResult(models.Model):
    team = models.CharField(_('Team'), max_length=1, choices=TEAMS)
    person = models.ManyToManyField(Person, through='Author')
    title = models.CharField(_('Title'), max_length=255)
    url = models.URLField(_('URL'), max_length=255, blank=True, null=True)
    note = models.CharField(_('Note'), max_length=255, blank=True, null=True)
    research_result_type = models.CharField(_('Type'), max_length=1, choices=TYPE, blank=True)
    ris_file_authors = models.CharField(_('RIS file authors'), max_length=255, blank=True, null=True)

    def __str__(self):
        return u'%s' % self.title

    def authors(self):
        if self.ris_file_authors != '':
            return self.ris_file_authors
        else:
            return '; '.join([str(name) for name in CitationName.objects.filter(
                person_id__in=self.person.all(),
                default_name=True)])


class Author(models.Model):
    author = models.ForeignKey(Person, on_delete=models.CASCADE)
    research_result = models.ForeignKey(ResearchResult, on_delete=models.CASCADE)
    order = models.IntegerField(_('Order of author'))

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')
        ordering = ('order', )


class Book(ResearchResult):
    """
    An instance of this class is a book.
    Similar to @book from bibtex.

    """
    type = models.CharField(_('Type'), max_length=1, choices=TYPE_BOOK_OR_CHAPTER)
    publisher = models.ForeignKey(Institution, verbose_name=_('Publisher'), on_delete=models.CASCADE)
    isbn = models.CharField(_('ISBN'), max_length=30, blank=True, null=True)
    volume = models.CharField(_('Volume/Number'), max_length=255, blank=True, null=True)
    serie = models.CharField(_('Serie'), max_length=255, blank=True, null=True)
    edition = models.CharField(_('Edition'), max_length=255, blank=True, null=True)
    doi = models.CharField(_('DOI'), max_length=255, blank=True, null=True)
    date = models.DateField(_('Date'), help_text='Date the book was published.')
    chapter = models.CharField(_('Chapter'), max_length=255, blank=True, null=True)
    start_page = models.IntegerField(_('Start page'), blank=True, null=True)
    end_page = models.IntegerField(_('End page'), blank=True, null=True)

    def __str__(self):
        return u'%s' % self.title

    class Meta:
        verbose_name = _('Book and chapter')
        verbose_name_plural = _('Books and chapters')

    # Sets the type of research result.
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.research_result_type = BOOK_OR_CHAPTER
        super(Book, self).save(*args, **kwargs)


class Periodical(models.Model):
    """
    An instance of this class is a journal or magazine.

    """
    name = models.CharField(_('Name'), max_length=255)
    acronym = models.CharField(_('Acronym'), max_length=50, blank=True, null=True)

    def __str__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('Periodical')
        verbose_name_plural = _('Periodicals')
        ordering = ('name', )


class PeriodicalRISFile(models.Model):
    """
    An instance of this class is how the RIS file called a journal or a magazine.

    """
    periodical = models.ForeignKey(Periodical, on_delete=models.CASCADE)
    name = models.CharField(_('Name'), max_length=255)

    def __str__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('Periodical name on the RIS file')
        verbose_name_plural = _('Periodical name on the RIS file')
        ordering = ('name', )


class Event(models.Model):
    """
    An instance of this class is a conference, a congress, a meeting or a symposium.
    Similar to @proceedings from bibtex.

    """
    name = models.CharField(_('Name'), max_length=255)
    acronym = models.CharField(_('Acronym'), max_length=50, blank=True, null=True)
    publisher = models.ForeignKey(
        Institution,
        verbose_name=_('Publisher'),
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    volume = models.CharField(_('Volume'), max_length=255, blank=True, null=True)
    number = models.CharField(_('Number'), max_length=255, blank=True, null=True)
    start_date = models.DateField(_('Start date of the event'))
    end_date = models.DateField(_('End date of the event'))
    local = models.CharField(_('Local'), max_length=255, help_text='Where the conference was held, '
                                                                   'e.g., "Rio de Janeiro, RJ, Brazil".')

    def __str__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events (congress, conference, etc.)')
        ordering = ('name', )


class EventRISFile(models.Model):
    """
    An instance of this class is how the RIS file called an event.

    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(_('Name'), max_length=255)

    def __str__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('Event name on the RIS file')
        verbose_name_plural = _('Event name on the RIS file')
        ordering = ('name', )


class Article(ResearchResult):
    """
    An instance of this class is a paper in a conference or in a journal.

    """
    periodical = models.ForeignKey(Periodical, verbose_name=_('Periodical'), blank=True, null=True,
                                   on_delete=models.CASCADE)
    event = models.ForeignKey(Event, verbose_name=_('Event'), blank=True, null=True,
                              help_text='Name of the conference, congress, meeting or symposium',
                              on_delete=models.CASCADE)
    type = models.CharField(_('Where?'), max_length=1, blank=True, null=True, choices=ARTICLE_TYPE)
    status = models.CharField(_('Status'), max_length=50)
    hide = models.BooleanField(_('Hide this paper in the report'), default=False)

    def __str__(self):
        return u'%s' % self.title

    def current_status(self):
        if u'p' in self.status:
            return _('Published')
        elif u'a' in self.status:
            return _('Accepted')
        elif u's' in self.status:
            return _('Submitted')
        elif u'd' in self.status:
            return _('Draft')

    def type_of_article(self):
        if self.type == PERIODICAL:
            return _('Periodical')
        elif self.type == EVENT:
            return _('Event')
        else:
            return _('Not defined')

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
        ordering = ('title', )

    # Sets the type of research result as article.
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.research_result_type = ARTICLE
        super(Article, self).save(*args, **kwargs)


class Draft(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    attachment = models.FileField(_('Attachment'), blank=True, null=True)
    date = models.DateField(_('Date'))

    class Meta:
        verbose_name = _('Draft')
        verbose_name_plural = _('Draft')


class Submitted(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    attachment = models.FileField(_('Attachment'), blank=True, null=True)
    date = models.DateField(_('Date'))

    class Meta:
        verbose_name = _('Submitted')
        verbose_name_plural = _('Submitted')


class Accepted(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE)
    attachment = models.FileField(_('Attachment'), blank=True, null=True)
    date = models.DateField(_('Date'))

    class Meta:
        verbose_name = _('Accepted')
        verbose_name_plural = _('Accepted')


class Published(models.Model):
    article = models.OneToOneField(Article, verbose_name=_('Article'), on_delete=models.CASCADE)
    doi = models.CharField(_('DOI'), max_length=255, blank=True, null=True)
    start_page = models.IntegerField(_('Start page'), blank=True, null=True)
    end_page = models.IntegerField(_('End page'), blank=True, null=True)
    attachment = models.FileField(_('Attachment'), blank=True, null=True)

    class Meta:
        verbose_name = _('Published')
        verbose_name_plural = _('Published')


class PublishedInPeriodical(Published):
    volume = models.CharField(_('Volume'), max_length=255, blank=True, null=True)
    number = models.CharField(_('Number'), max_length=255, blank=True, null=True)
    date = models.DateField(_('Date'))


class TypeAcademicWork(models.Model):
    """
    An instance of this class is a type of academic work.

    """
    name = models.CharField(_('Name'), max_length=255)

    def __str__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('Type of Academic Work')
        verbose_name_plural = _('Types of Academic Work')
        ordering = ('name', )


class AcademicWork(models.Model):
    """
    An instance of this class is an academic work.

    """
    type = models.ForeignKey(TypeAcademicWork, verbose_name=_('Type'), on_delete=models.CASCADE)
    title = models.CharField(_('Title'), max_length=255)
    advisee = models.ForeignKey(Person, verbose_name=_('Advisee'), on_delete=models.CASCADE)
    advisor = models.ForeignKey(
        Person,
        verbose_name=_('Advisor'),
        related_name='advisor_academic_work',
        on_delete=models.CASCADE)
    co_advisor = models.ManyToManyField(Person, verbose_name=_('Co-Advisor'), related_name='co_advisor_academic_work',
                                        blank=True)
    funding = models.BooleanField(_('Financially supported?'), choices=FUNDING_CHOICES, max_length=3)
    funding_agency = models.CharField(_('Funding agency'), max_length=255, blank=True)
    url = models.URLField(_('URL'), max_length=255, blank=True, null=True, help_text='URL to funding information.')
    start_date = models.DateField(_('Start date'))
    end_date = models.DateField(_('End date'), blank=True, null=True)
    abstract = models.TextField(_('Abstract'))

    def __str__(self):
        return u'%s' % self.title

    def co_advisors(self):
        return ', '.join([co_advisor.full_name for co_advisor in self.co_advisor.all()])

    class Meta:
        verbose_name = _('Academic Work')
        verbose_name_plural = _('Academic Works')
        ordering = ('-start_date', )
