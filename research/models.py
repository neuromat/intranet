from django.db import models
from django.utils.translation import ugettext_lazy as _
from person.models import Person, Institution
from django.utils.html import format_html


# Defining types of research results
ARTICLE = 'a'
BOOK = 'b'
BOOK_CHAPTER = 'c'
TYPE = (
    (ARTICLE, _('Article')),
    (BOOK, _('Book')),
    (BOOK_CHAPTER, _('Book chapter')),
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


class ResearchResult(models.Model):
    team = models.CharField(_('Team'), max_length=1, choices=TEAMS)
    person = models.ManyToManyField(Person, through='Author')
    title = models.CharField(_('Title'), max_length=255)
    url = models.URLField(_('URL'), max_length=255, blank=True, null=True)
    note = models.CharField(_('Note'), max_length=255, blank=True, null=True)
    research_result_type = models.CharField(_('Type'), max_length=1, choices=TYPE, blank=True)

    def __unicode__(self):
        return u'%s' % self.title

    def authors(self):
        return format_html("; ".join([unicode(person.citation_name if person.citation_name else person.full_name)
                                      for person in self.person.all().order_by('author__order')]))

    authors.allow_tags = True


class Author(models.Model):
    author = models.ForeignKey(Person)
    research_result = models.ForeignKey(ResearchResult)
    order = models.IntegerField(_('Order of author'))

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')
        ordering = ('order', )


class Event(models.Model):
    """
    An instance of this class is a conference, a congress, a meeting or a symposium.
    Similar to @proceedings from bibtex.

    """
    name = models.CharField(_('Name'), max_length=255)
    acronym = models.CharField(_('Acronym'), max_length=50, blank=True, null=True)
    start_date = models.DateField(_('Start date of the event'))
    end_date = models.DateField(_('End date of the event'))
    local = models.CharField(_('Local'), max_length=255, help_text='Where the conference was held, '
                                                                   'e.g., "Rio de Janeiro, RJ, Brazil".')

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events (congress, conference, etc.)')
        ordering = ('name', )


class Journal(models.Model):
    """
    An instance of this class is a journal.

    """
    name = models.CharField(_('Name'), max_length=255)
    acronym = models.CharField(_('Acronym'), max_length=50, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('Journal')
        verbose_name_plural = _('Journals')
        ordering = ('name', )


class Article(ResearchResult):
    """
    An instance of this class is a paper in a conference or in a journal.

    """
    journal = models.ForeignKey(Journal, verbose_name=_('Journal'), blank=True, null=True)
    event = models.ForeignKey(Event, verbose_name=_('Event'), blank=True, null=True,
                              help_text='Name of the conference, congress, meeting or symposium')

    def __unicode__(self):
        return u'%s' % self.title

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
    article = models.OneToOneField(Article, verbose_name=_('Article'))
    attachment = models.FileField(_('Attachment'), blank=True, null=True)
    date = models.DateField(_('Date'))

    class Meta:
        verbose_name = _('Draft')
        verbose_name_plural = _('Draft')


class Submitted(models.Model):
    article = models.ForeignKey(Article, verbose_name=_('Article'))
    attachment = models.FileField(_('Attachment'), blank=True, null=True)
    date = models.DateField(_('Date'))

    class Meta:
        verbose_name = _('Submitted')
        verbose_name_plural = _('Submitted')


class Accepted(models.Model):
    article = models.OneToOneField(Article, verbose_name=_('Article'))
    attachment = models.FileField(_('Attachment'), blank=True, null=True)
    date = models.DateField(_('Date'))

    class Meta:
        verbose_name = _('Accepted')
        verbose_name_plural = _('Accepted')


class Published(models.Model):
    article = models.OneToOneField(Article, verbose_name=_('Article'))
    volume = models.CharField(_('Volume'), max_length=255, blank=True, null=True)
    number = models.CharField(_('Number'), max_length=255, blank=True, null=True)
    doi = models.CharField(_('DOI'), max_length=255, blank=True, null=True)
    start_page = models.IntegerField(_('Start page'), blank=True, null=True)
    end_page = models.IntegerField(_('End page'), blank=True, null=True)
    attachment = models.FileField(_('Attachment'), blank=True, null=True)
    date = models.DateField(_('Date'))

    class Meta:
        verbose_name = _('Published')
        verbose_name_plural = _('Published')


class Book(ResearchResult):
    """
    An instance of this class is a book.
    Similar to @book from bibtex.

    """
    publisher = models.ForeignKey(Institution, verbose_name=_('Publisher'))
    isbn = models.CharField(_('ISBN'), max_length=30, blank=True, null=True)
    volume = models.CharField(_('Volume/Number'), max_length=255, blank=True, null=True)
    serie = models.CharField(_('Serie'), max_length=255, blank=True, null=True)
    edition = models.CharField(_('Edition'), max_length=255, blank=True, null=True)
    doi = models.CharField(_('DOI'), max_length=255, blank=True, null=True)
    date = models.DateField(_('Date'), help_text='Date the book was published.')

    def __unicode__(self):
        return u'%s' % self.title

    class Meta:
        verbose_name = _('Book')
        verbose_name_plural = _('Books')

    # Sets the type of research result.
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.research_result_type = BOOK
        super(Book, self).save(*args, **kwargs)


class BookChapter(models.Model):
    """
    An instance of this class is a book chapter.
    Similar to @inbook from bibtex.

    """
    book = models.ForeignKey(Book, verbose_name=_('Book'))
    chapter = models.CharField(_('Chapter'), max_length=255, blank=True, null=True)
    start_page = models.IntegerField(_('Start page'), blank=True, null=True)
    end_page = models.IntegerField(_('End page'), blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.chapter

    class Meta:
        verbose_name = _('Book chapter')
        verbose_name_plural = _('Book chapters')

    # Sets the type of research result.
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.research_result_type = BOOK_CHAPTER
        super(BookChapter, self).save(*args, **kwargs)


class TypeAcademicWork(models.Model):
    """
    An instance of this class is a type of academic work.

    """
    name = models.CharField(_('Name'), max_length=255)

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
    advisee = models.ForeignKey(Person, verbose_name=_('Advisee'))
    advisor = models.ForeignKey(Person, verbose_name=_('Advisor'), related_name='advisor_academic_work')
    co_advisor = models.ManyToManyField(Person, verbose_name=_('Co-Advisor'), related_name='co_advisor_academic_work',
                                        blank=True, null=True)
    schollarship = models.CharField(_('Schollarship'), max_length=255, blank=True, null=True)
    start_date = models.DateField(_('Start date'))
    end_date = models.DateField(_('End date'), blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.title

    def co_advisors(self):
        return ', '.join([unicode(co_advisor.full_name) for co_advisor in self.co_advisor.all()])

    class Meta:
        verbose_name = _('Academic Work')
        verbose_name_plural = _('Academic Works')
        ordering = ('-start_date', )
