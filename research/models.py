from django.db import models
from django.utils.translation import ugettext_lazy as _
from person.models import Person, Institution
import datetime
from django.utils.html import format_html
from django.utils.dates import MONTHS

# Defining types of status
IN_PROGRESS = 'i'
CONCLUDED = 'c'
STATUS_ANSWER = (
    (IN_PROGRESS, _('In Progress')),
    (CONCLUDED, _('Concluded')),
)

# Defining types of research results
UNPUBLISHED = 'u'
PUBLISHED = 'p'
RESEARCH_RESULT_TYPE = (
    (UNPUBLISHED, _('Unpublished')),
    (PUBLISHED, _('Published')),
)

# Defining types of status for article (Published)
ACCEPTED = 'a'
PUBLISHED_STATUS = (
    (ACCEPTED, _('Accepted')),
    (PUBLISHED, _('Published')),
)

# Defining types of status for article (Unpublished)
DRAFT = 'd'
SUBMITTED = 's'
UNPUBLISHED_STATUS = (
    (DRAFT, _('Draft')),
    (SUBMITTED, _('Submitted')),
)

# Defining types of research results
ARTICLE = 'a'
MEETING = 'm'
BOOK = 'b'
IN_BOOK = 'i'
TYPE = (
    (ARTICLE, _('Article')),
    (MEETING, _('Communication in meeting')),
    (BOOK, _('Book')),
    (IN_BOOK, _('In book')),
)

# Year to be displayed
YEAR_CHOICES = []
for year in range(2013, (datetime.datetime.now().year+1)):
    YEAR_CHOICES.append((year, year))
YEAR_CHOICES.reverse()


class ResearchResult(models.Model):
    """
    '__unicode__'		Returns the title.
    'class Meta'		Ordering of data by date modification.
    """
    person = models.ManyToManyField(Person, through='Author')
    title = models.CharField(_('Title'), max_length=255)
    year = models.IntegerField(_('Year'), max_length=4, choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    month = models.SmallIntegerField(_('Month'), choices=MONTHS.items())
    url = models.URLField(_('URL'), max_length=255, blank=True, null=True)
    key = models.CharField(_('Key'), max_length=255, blank=True, null=True)
    note = models.CharField(_('Note'), max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(default=datetime.datetime.now)
    research_result_type = models.CharField(_('Type'), max_length=1, choices=RESEARCH_RESULT_TYPE, blank=True)

    def __unicode__(self):
        return u'%s' % self.title

    def authors(self):
        return format_html("; ".join([unicode(person.citation_name if person.citation_name else person.full_name)
                                      for person in self.person.all().order_by('author__order')]))

    authors.allow_tags = True

    # Description of the model / Sort by title
    class Meta:
        ordering = ('-modified', )


class Author(models.Model):
    author = models.ForeignKey(Person)
    research_result = models.ForeignKey(ResearchResult)
    order = models.IntegerField(_('Order of author'))

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')
        ordering = ('order', )


class Published(ResearchResult):
    reference = models.TextField(_('Reference to NeuroMat'), blank=True, null=True,
                                 help_text='You should copy here the lines of your work that makes reference to CEPID '
                                           'NeuroMat, e.g., "this article (thesis,...) was produced as part of the '
                                           'activities of FAPESP Center for Neuromathematics (grant #2013/07699-0, '
                                           'S.Paulo Research Foundation)".')
    published_type = models.CharField(_('Type'), max_length=1, choices=TYPE, blank=True)

    # Sets the type of research result as published.
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.research_result_type = PUBLISHED
        super(Published, self).save(*args, **kwargs)


class Unpublished(ResearchResult):
    """
    An instance of this class is a document having an author and title, but not formally published.

    """
    type = models.CharField(_('Type'), max_length=1, choices=TYPE, blank=True)
    status = models.CharField(_('Status'), max_length=1, choices=STATUS_ANSWER, default=IN_PROGRESS,
                              blank=True, null=True)
    paper_status = models.CharField(_('Paper status'), max_length=1, choices=UNPUBLISHED_STATUS, blank=True, null=True)

    class Meta:
        verbose_name = _('Unpublished')
        verbose_name_plural = _('Unpublished')

    # Sets the type of research result as unpublished.
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.research_result_type = UNPUBLISHED
        super(Unpublished, self).save(*args, **kwargs)


class InProceeding(Published):
    """
    An instance of this class is an article in a conference proceedings.

    """
    doi = models.CharField(_('DOI'), max_length=255, blank=True, null=True)
    address = models.CharField(_('Address'), max_length=255, blank=True, null=True,
                               help_text='Where the conference was held, e.g., "Nagoya, Japan".')
    book_title = models.CharField(_('Book title'), max_length=255)
    editor = models.CharField(_('Editor'), max_length=255, blank=True, null=True)
    volume = models.CharField(_('Volume'), max_length=255, blank=True, null=True)
    number = models.CharField(_('Number'), max_length=255, blank=True, null=True)
    serie = models.CharField(_('Serie'), max_length=255, blank=True, null=True)
    start_page = models.IntegerField(_('Start page'), blank=True, null=True)
    end_page = models.IntegerField(_('End page'), blank=True, null=True)
    attachment = models.FileField(_('Attachment'), blank=True, null=True)
    publisher = models.ForeignKey(Institution, related_name='published_by', verbose_name=_('Publisher'),
                                  blank=True, null=True)
    organization = models.ForeignKey(Institution, related_name='sponsored_by', verbose_name=_('Organization'),
                                     blank=True, null=True)

    class Meta:
        verbose_name = _('Communication in meeting')
        verbose_name_plural = _('Communications in meetings')

    # Sets the type of research result.
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.published_type = MEETING
        super(InProceeding, self).save(*args, **kwargs)


class Journal(models.Model):
    """
    An instance of this class is a journal.

    """
    name = models.CharField(_('Name'), max_length=255)

    # Returns the name
    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('Journal')
        verbose_name_plural = _('Journals')
        ordering = ('name', )


class Article(Published):
    """
    An instance of this class is a paper published by a journal.

    """
    journal = models.ForeignKey(Journal, verbose_name=_('Journal'))
    status = models.CharField(_('Status'), max_length=1, choices=PUBLISHED_STATUS)
    doi = models.CharField(_('DOI'), max_length=255, blank=True, null=True)
    number = models.CharField(_('Number'), max_length=255, blank=True, null=True)
    volume = models.CharField(_('Volume'), max_length=255, blank=True, null=True)
    start_page = models.IntegerField(_('Start page'), blank=True, null=True)
    end_page = models.IntegerField(_('End page'), blank=True, null=True)
    attachment = models.FileField(_('Attachment'), blank=True, null=True)

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')

    # Sets the type of research result.
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.published_type = ARTICLE
        super(Article, self).save(*args, **kwargs)


class Book(Published):
    """
    An instance of this class is a book or a chapter of a book.

    """
    publisher = models.ForeignKey(Institution, verbose_name=_('Publisher'))
    doi = models.CharField(_('DOI'), max_length=255, blank=True, null=True)
    editor = models.CharField(_('Editor'), max_length=255, blank=True, null=True)
    volume = models.CharField(_('Volume'), max_length=255, blank=True, null=True)
    serie = models.CharField(_('Serie'), max_length=255, blank=True, null=True)
    edition = models.CharField(_('Edition'), max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _('Book')
        verbose_name_plural = _('Books')

    # Sets the type of research result.
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.published_type = BOOK
        super(Book, self).save(*args, **kwargs)


class InBook(models.Model):
    book = models.ForeignKey(Book, verbose_name=_('Book'))
    chapter = models.CharField(_('Chapter'), max_length=255, blank=True, null=True)
    start_page = models.IntegerField(_('Start page'), blank=True, null=True)
    end_page = models.IntegerField(_('End page'), blank=True, null=True)

    class Meta:
        verbose_name = _('Inbook')
        verbose_name_plural = _('Inbooks')


class TypeAcademicWork(models.Model):
    """
    An instance of this class is a type of academic work.

    """
    name = models.CharField(_('Name'), max_length=255)

    # Returns the name
    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('Type of Academic Work')
        verbose_name_plural = _('Types of Academic Work')
        ordering = ('name', )


class AcademicWork(models.Model):
    """
    An instance of this class is an academic work.

    """
    type = models.ForeignKey(TypeAcademicWork, verbose_name=_('Type'))
    title = models.CharField(_('Title'), max_length=255)
    author = models.ForeignKey(Person, verbose_name=_('Author'))
    advisor = models.ForeignKey(Person, verbose_name=_('Advisor'), related_name='advisor_academic_work')
    co_advisor = models.ManyToManyField(Person, verbose_name=_('Co-Advisor'),
                                        related_name='co_advisor_academic_work', blank=True, null=True)
    institution = models.ForeignKey(Institution, verbose_name=_('Institution'))
    status = models.CharField(_('Status'), max_length=1, choices=STATUS_ANSWER)
    schollarship = models.CharField(_('Schollarship'), max_length=255, blank=True, null=True)
    start_date = models.DateField(_('Start date'))
    end_date = models.DateField(_('End date'))

    class Meta:
        verbose_name = _('Academic Work')
        verbose_name_plural = _('Academic Works')
