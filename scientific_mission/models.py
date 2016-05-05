from activity.models import ProjectActivities
from cities_light.models import City, Country, Region
from person.models import Person
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Type(models.Model):
    """
    An instance of this class is a type of scientific mission.

    '__unicode__'		Returns the mission.
    'class Meta'		Sets the description (singular and plural) model and the ordering of data by mission.
    """
    mission = models.CharField(_('Scientific Mission'), max_length=255, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.mission

    class Meta:
        verbose_name = _('Type of scientific mission')
        verbose_name_plural = _('Types of scientific mission')
        ordering = ('mission', )


class ScientificMission(models.Model):
    """
    An instance of this class is a daily stipend paid to a person.

    """
    person = models.ForeignKey(Person, verbose_name=_('Paid to'))
    mission = models.ForeignKey(Type, verbose_name=_('Mission'), blank=True, null=True)
    project_activity = models.ForeignKey(ProjectActivities, verbose_name=_('Project activity'), blank=True, null=True)
    origin_country = models.ForeignKey(Country, verbose_name=_('Country of origin'))
    origin_city = models.ForeignKey(City, verbose_name=_('City of origin'))
    destination_country = models.ForeignKey(Country, verbose_name=_('Country of destination'),
                                            related_name='destination_country')
    destination_city = models.ForeignKey(City, verbose_name=_('City of destination'), related_name='destination_city')
    departure = models.DateTimeField(_('Departure'))
    arrival = models.DateTimeField(_('Arrival'))
    amount_paid = models.DecimalField(_('Amount paid'), max_digits=10, decimal_places=2)

    def __unicode__(self):
        return u'%s' % self.person

    class Meta:
        verbose_name = _('Daily stipend')
        verbose_name_plural = _('Daily stipends')
        ordering = ('person', )

    def value(self):
        return "R$ %s" % self.amount_paid

