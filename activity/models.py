from django.db import models
from django.utils.translation import ugettext_lazy as _
from member.models import Investigator, Institution


class TrainingProgram(models.Model):
    """
    An instance of this class is a training program.

    """
    investigator = models.ForeignKey(Investigator, verbose_name=_('Speaker'))
    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'), max_length=500, blank=True, null=True)
    start_date = models.DateField(_('Start date'))
    end_date = models.DateField(_('End date'), blank=True, null=True)
    local = models.ForeignKey(Institution, verbose_name=_('Local'), blank=True, null=True)
    duration = models.CharField(_('Duration'), max_length=20)

    def __unicode__(self):
        return u'%s' % self.investigator

    class Meta:
        verbose_name = _('Training Program')
        verbose_name_plural = _('Training Programs')
        ordering = ('investigator', )


class Seminar(models.Model):
    """
    An instance of this class is a seminar.

    """
    investigator = models.ForeignKey(Investigator, verbose_name=_('Speaker'))
    title = models.CharField(_('Title'), max_length=200)
    abstract = models.TextField(_('Abstract'), max_length=500, blank=True, null=True)
    date = models.DateField(_('Date'))
    attachment = models.FileField(_('Attachment'))

    def __unicode__(self):
        return u'%s' % self.investigator

    class Meta:
        verbose_name = _('Seminar')
        verbose_name_plural = _('Seminars')
        ordering = ('investigator', )


class ScientificMission(models.Model):
    """
    An instance of this class is a scientific mission.

    """
    investigator = models.ForeignKey(Investigator, verbose_name=_('Investigator'))
    mission = models.TextField(_('Mission'), max_length=500)
    start_date = models.DateField(_('Start date'))
    end_date = models.DateField(_('End date'))

    def __unicode__(self):
        return u'%s' % self.investigator

    class Meta:
        verbose_name = _('Scientific mission')
        verbose_name_plural = _('Scientific missions')
        ordering = ('investigator', )


class Meeting(models.Model):
    """
    An instance of this class is a meeting.

    """
    local = models.ManyToManyField(Institution, verbose_name=_('Local'), blank=True, null=True)
    speaker = models.ManyToManyField(Investigator, verbose_name=_('Speaker'), blank=True, null=True)
    participant = models.ManyToManyField(Investigator, verbose_name=_('Participant'), blank=True, null=True)
    title = models.CharField(_('Title'), max_length=200)
    start_date = models.DateField(_('Start date'))
    end_date = models.DateField(_('End date'))
    description = models.TextField(_('Description'), max_length=500)
    url = models.URLField(_('URL'), blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.title

    class Meta:
        verbose_name = _('Meeting')
        verbose_name_plural = _('Meetings')
        ordering = ('start_date', )


class GeneralEvent(models.Model):
    """
    An instance of this class is a general event.

    """
    speaker = models.ManyToManyField(Investigator, verbose_name=_('Speaker'))
    local = models.ForeignKey(Institution, verbose_name=_('Local'), blank=True, null=True)
    title = models.CharField(_('Title'), max_length=200)
    start_date = models.DateField(_('Start date'))
    end_date = models.DateField(_('End date'), blank=True, null=True)
    description = models.TextField(_('Description'), max_length=500, blank=True, null=True)
    url = models.URLField(_('URL'), blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.title

    class Meta:
        verbose_name = _('General event')
        verbose_name_plural = _('General events')
        ordering = ('start_date', )