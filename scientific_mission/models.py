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

    '__unicode__'		Returns the person and the amount paid.
    'class Meta'		Sets the description (singular and plural) model and the ordering of data by
                        date_of_registration.
    'value'             Returns the symbol for the Brazilian currency and the amount paid
    """
    person = models.ForeignKey(Person, verbose_name=_('Paid to'), on_delete=models.CASCADE)
    mission = models.ForeignKey(Type, verbose_name=_('Mission'), blank=True, null=True, on_delete=models.CASCADE)
    project_activity = models.ForeignKey(ProjectActivities, verbose_name=_('Project activity'), blank=True, null=True,
                                         on_delete=models.CASCADE)
    destination_city = models.ForeignKey(City, verbose_name=_('City of destination'), null=True,
                                         related_name='destination_city', on_delete=models.CASCADE)
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
    """
    An instance of this class is a route on a scientific mission.

    'class Meta'		Ordering of route by scientific_mission and order.
    'save'              Set an integer value to order
    """
    scientific_mission = models.ForeignKey(ScientificMission, on_delete=models.CASCADE)
    origin_city = models.ForeignKey(City, related_name='origin', verbose_name=_('From'), on_delete=models.CASCADE)
    destination_city = models.ForeignKey(City, related_name='destination', verbose_name=_('To'), on_delete=models.CASCADE)
    departure = models.DateTimeField(_('Departure'))
    arrival = models.DateTimeField(_('Arrival'))
    order = models.PositiveIntegerField(_('Order'))

    class Meta:
        ordering = ('scientific_mission', 'order')

    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.order = self.order
        else:
            last_order = Route.objects.filter(scientific_mission=self.scientific_mission).order_by('-order').first()
            self.order = last_order.order + 1 if last_order else 1
        super(Route, self).save(*args, **kwargs)
