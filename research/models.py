from django.db import models
from django.utils.translation import ugettext_lazy as _
from member.models import Investigator
import datetime

# Create your models here.

IN_PROGRESS = 'i'
CONCLUDED = 'c'
STATUS_ANSWER = (
    (IN_PROGRESS, _('In Progress')),
    (CONCLUDED, _('Concluded')),
)


class Document(models.Model):
    """
    Abstract class.

    '__unicode__'		Returns the title.
    'class Meta'		Sets the class as abstract and the ordering of data by date of modification.
    """
    title = models.CharField(_('Title'), max_length=200)
    reference = models.TextField(_('Reference to NeuroMat'),
                                 help_text='You should copy here the lines of your work that makes reference to CEPID '
                                           'NeuroMat, e.g., "this article (thesis,...) was produced as part of the '
                                           'activities of FAPESP Center for Neuromathematics (grant #2013/07699-0, '
                                           'S.Paulo Research Foundation)".')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return u'%s' % self.title

    # Description of the model / Sort by title
    class Meta:
        abstract = True
        ordering = ('modified', )


class PaperStatus(models.Model):
    name = models.CharField(_('Name'), max_length=50)

    # Returns the name
    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('Paper status')
        verbose_name_plural = _('Papers status')
        ordering = ('name', )


class Paper(Document):
    """
    An instance of this class is a paper.

    """
    author = models.ManyToManyField(Investigator, verbose_name=_('Author'))
    status = models.ForeignKey(PaperStatus, verbose_name=_('Status'))
    doi = models.CharField(_('DOI'), max_length=50, blank=True, null=True)
    issn = models.CharField(_('ISSN'), max_length=50, blank=True, null=True)
    local = models.CharField(_('Local'), max_length=50, blank=True, null=True)
    volume = models.CharField(_('Volume'), max_length=50, blank=True, null=True)
    issue = models.CharField(_('Issue'), max_length=50, blank=True, null=True)
    start_page = models.IntegerField(_('Start page'), max_length=6, blank=True, null=True)
    end_page = models.IntegerField(_('End page'), max_length=6, blank=True, null=True)
    year = models.IntegerField(_('Year'), max_length=4, blank=True, null=True)
    url = models.URLField(_('URL'), max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = _('Paper')

    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = Paper.objects.get(pk=self.pk)
            if orig.status != self.status:
                self.modified = datetime.datetime.now()
        super(Paper, self).save(*args, **kwargs)


class TypeAcademicWork(models.Model):
    name = models.CharField(_('Name'), max_length=50)

    # Returns the name
    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('Type of academic work')
        verbose_name_plural = _('Types of academic work')
        ordering = ('name', )


class AcademicWork(Document):
    """
    An instance of this class is an academic work.

    """
    type = models.ForeignKey(TypeAcademicWork, verbose_name=_('Type of academic work'))
    author = models.ForeignKey(Investigator, verbose_name=_('Author'))
    supervisor = models.ForeignKey(Investigator, verbose_name=_('Supervisor'), related_name='supervisor_academic_work')
    co_supervisor = models.ManyToManyField(Investigator, verbose_name=_('Co-Supervisor'),
                                           related_name='co_supervisor_academic_work', blank=True, null=True)
    status = models.CharField(_('Status'), max_length=1, choices=STATUS_ANSWER)

    class Meta:
        verbose_name = _('Academic Work')
        verbose_name_plural = _('Academic Works')

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
    author = models.ForeignKey(Investigator, verbose_name=_('Author'))
    description = models.TextField(_('Description'), max_length=500)
    status = models.CharField(_('Status'), max_length=1, choices=STATUS_ANSWER)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return u'%s' % self.author

    class Meta:
        verbose_name = _('Work in Progress')
        verbose_name_plural = _('Works in Progress')
        ordering = ('modified', )

    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = WorkInProgress.objects.get(pk=self.pk)
            if orig.status != self.status:
                self.modified = datetime.datetime.now()
        super(WorkInProgress, self).save(*args, **kwargs)