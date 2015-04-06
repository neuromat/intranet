from django.db import models
from django.utils.translation import ugettext_lazy as _
from member.models import Person, ProjectMember
import datetime

# Defining types of status
IN_PROGRESS = 'i'
CONCLUDED = 'c'
STATUS_ANSWER = (
    (IN_PROGRESS, _('In Progress')),
    (CONCLUDED, _('Concluded')),
)

# Defining types of paper status
DRAFT = 'd'
SUBMITTED = 's'
PUBLISHED = 'p'
PAPER_STATUS = (
    (DRAFT, _('Draft')),
    (SUBMITTED, _('Submitted')),
    (PUBLISHED, _('Published')),
)

# Defining types of research results
BOOK = 'b'
PAPER = 'p'
CHAPTER = 'c'
RESEARCH_RESULT_TYPE = (
    (BOOK, _('Book / Book Chapters')),
    (PAPER, _('Paper')),
)
BOOK_OR_CHAPTER = (
    (BOOK, _('Book')),
    (CHAPTER, _('Book Chapter')),
)


class ResearchResult(models.Model):
    """
    '__unicode__'		Returns the title.
    'class Meta'		Ordering of data by date modification.
    """
    author = models.ManyToManyField(Person)
    title = models.CharField(_('Title'), max_length=255)
    doi = models.CharField(_('DOI'), max_length=255, blank=True, null=True)
    serie = models.CharField(_('Serie'), max_length=50, blank=True, null=True)
    volume = models.CharField(_('Volume'), max_length=255, blank=True, null=True)
    issue = models.CharField(_('Issue'), max_length=255, blank=True, null=True)
    publisher = models.CharField(_('Publisher'), max_length=255, blank=True, null=True)
    start_page = models.IntegerField(_('Start page'), blank=True, null=True)
    end_page = models.IntegerField(_('End page'), blank=True, null=True)
    year = models.IntegerField(_('Year'), blank=True, null=True)
    url = models.URLField(_('URL'), max_length=255, blank=True, null=True)
    reference = models.TextField(_('Reference to NeuroMat'),
                                 help_text='You should copy here the lines of your work that makes reference to CEPID '
                                           'NeuroMat, e.g., "this article (thesis,...) was produced as part of the '
                                           'activities of FAPESP Center for Neuromathematics (grant #2013/07699-0, '
                                           'S.Paulo Research Foundation)".')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(default=datetime.datetime.now)
    research_result_type = models.CharField(_('Type'), max_length=1, choices=RESEARCH_RESULT_TYPE, blank=True)

    def __unicode__(self):
        return u'%s' % self.title

    # Description of the model / Sort by title
    class Meta:
        ordering = ('-modified', )


class Paper(ResearchResult):
    """
    An instance of this class is a paper.

    """
    status = models.CharField(_('Status'), max_length=1, choices=PAPER_STATUS)
    issn = models.CharField(_('ISSN'), max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _('Paper')
        verbose_name_plural = _('Papers')

    # Sets the type of research result.
    # Check if the status has changed to update the modified date.
    def save(self, *args, **kwargs):
        self.research_result_type = PAPER
        if self.pk is not None:
            orig = Paper.objects.get(pk=self.pk)
            if orig.status != self.status:
                self.modified = datetime.datetime.now()
        super(Paper, self).save(*args, **kwargs)


class Book(ResearchResult):
    """
    An instance of this class is a book or a chapter of a book.

    """
    book_or_chapter = models.CharField(_('Type'), max_length=1, choices=BOOK_OR_CHAPTER)
    status = models.CharField(_('Status'), max_length=1, choices=STATUS_ANSWER)
    isbn = models.CharField(_('ISBN'), max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _('Book / Book Chapter')
        verbose_name_plural = _('Books / Book Chapters')

    # Sets the type of research result.
    # Check if the status has changed to update the modified date.
    def save(self, *args, **kwargs):
        self.research_result_type = BOOK
        if self.pk is not None:
            orig = Book.objects.get(pk=self.pk)
            if orig.status != self.status:
                self.modified = datetime.datetime.now()
        super(Book, self).save(*args, **kwargs)


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
    status = models.CharField(_('Status'), max_length=1, choices=STATUS_ANSWER)
    reference = models.TextField(_('Reference to NeuroMat'),
                                 help_text='You should copy here the lines of your work that makes reference to CEPID '
                                           'NeuroMat, e.g., "this article (thesis,...) was produced as part of the '
                                           'activities of FAPESP Center for Neuromathematics (grant #2013/07699-0, '
                                           'S.Paulo Research Foundation)".')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        verbose_name = _('Academic Work')
        verbose_name_plural = _('Academic Works')

    # Check if the status has changed to update the modified date.
    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = AcademicWork.objects.get(pk=self.pk)
            if orig.status != self.status:
                self.modified = datetime.datetime.now()
        super(AcademicWork, self).save(*args, **kwargs)


class WorkInProgress(models.Model):
    """
    An instance of this class is a work in progress.

    """
    author = models.ForeignKey(ProjectMember, verbose_name=_('Author'))
    description = models.TextField(_('Description'))
    status = models.CharField(_('Status'), max_length=1, choices=STATUS_ANSWER)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return u'%s' % self.author

    class Meta:
        verbose_name = _('Work in Progress')
        verbose_name_plural = _('Works in Progress')
        ordering = ('modified', )

    # Check if the status has changed to update the modified date.
    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = WorkInProgress.objects.get(pk=self.pk)
            if orig.status != self.status:
                self.modified = datetime.datetime.now()
        super(WorkInProgress, self).save(*args, **kwargs)
