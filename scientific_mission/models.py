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
    destination_city = models.ForeignKey(City, verbose_name=_('City of destination'))
    amount_paid = models.DecimalField(_('Amount paid'), max_digits=10, decimal_places=2)
    date_of_registration = models.DateTimeField(_('Date'), auto_now_add=True, null=True)

    def __unicode__(self):
        return u'%s - R$ %s' % (self.person, self.amount_paid)

    class Meta:
        verbose_name = _('Daily stipend')
        verbose_name_plural = _('Daily stipends')
        ordering = ('-date_of_registration',)

    def value(self):
        return "R$ %s" % self.amount_paid


class Route(models.Model):
    scientific_mission = models.ForeignKey(ScientificMission)
    origin_city = models.ForeignKey(City, related_name='origin', verbose_name=_('From'))
    destination_city = models.ForeignKey(City, related_name='destination', verbose_name=_('To'))
    departure = models.DateTimeField(_('Departure'))
    arrival = models.DateTimeField(_('Arrival'))
    order = models.PositiveIntegerField(_('Order'))
