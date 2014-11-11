from django.db import models
from django.utils.translation import ugettext_lazy as _
from member.models import Investigator


class TrainingProgram(models.Model):
    """
    An instance of this class is a training program.

    """
    speaker = models.ForeignKey(Investigator, verbose_name=_('Speaker'))
    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'), max_length=500, blank=True, null=True)
    date = models.DateField(_('Date'))
    duration = models.CharField(_('Duration'), max_length=20)

    def __unicode__(self):
        return u'%s' % self.speaker

    class Meta:
        verbose_name = _('Training Program')
        verbose_name_plural = _('Training Programs')
        ordering = ('speaker', )


class Seminar(models.Model):
    """
    An instance of this class is a seminar.

    """
    speaker = models.ForeignKey(Investigator, verbose_name=_('Speaker'))
    title = models.CharField(_('Title'), max_length=200)
    abstract = models.TextField(_('Abstract'), max_length=500, blank=True, null=True)
    date = models.DateField(_('Date'))

    def __unicode__(self):
        return u'%s' % self.speaker

    class Meta:
        verbose_name = _('Seminar')
        verbose_name_plural = _('Seminars')
        ordering = ('speaker', )


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