from django.db import models
from django.utils.translation import ugettext_lazy as _
from custom_user.models import Person, Institution
from django.utils.html import format_html
from django.conf import settings

# Defining the duration of a Training Program
ONE_HOUR = '1h'
ONE_AND_A_HALF_HOUR = '1h30'
TWO_HOURS = '2h'
TWO_AND_A_HALF_HOURS = '2h30'
THREE_HOURS = '3h'
THREE_AND_A_HALF_HOURS = '3h30'
FOUR_HOURS = '4h'
FOUR_AND_A_HALF_HOURS = '4h30'
FIVE_HOURS = '5h'
FIVE_AND_A_HALF_HOURS = '5h30'
SIX_HOURS = '6h'
SIX_AND_A_HALF_HOURS = '6h30'
SEVEN_HOURS = '7h'
SEVEN_AND_A_HALF_HOURS = '7h30'
EIGHT_HOURS = '8h'
EIGHT_AND_A_HALF_HOURS = '8h30'
NINE_HOURS = '9h'
NINE_AND_A_HALF_HOURS = '9h30'
TEN_HOURS = '10h'
OTHER = 'Other'
DURATION = (
    (ONE_HOUR, '1h'),
    (ONE_AND_A_HALF_HOUR, '1h30'),
    (TWO_HOURS, '2h'),
    (TWO_AND_A_HALF_HOURS, '2h30'),
    (THREE_HOURS, '3h'),
    (THREE_AND_A_HALF_HOURS, '3h30'),
    (FOUR_HOURS, '4h'),
    (FOUR_AND_A_HALF_HOURS, '4h30'),
    (FIVE_HOURS, '5h'),
    (FIVE_AND_A_HALF_HOURS, '5h30'),
    (SIX_HOURS, '6h'),
    (SIX_AND_A_HALF_HOURS, '6h30'),
    (SEVEN_HOURS, '7h'),
    (SEVEN_AND_A_HALF_HOURS, '7h30'),
    (EIGHT_HOURS, '8h'),
    (EIGHT_AND_A_HALF_HOURS, '8h30'),
    (NINE_HOURS, '9h'),
    (NINE_AND_A_HALF_HOURS, '9h30'),
    (TEN_HOURS, '10h'),
    (OTHER, _('Other duration time'))
)

# Defining types of activities
TRAINING_PROGRAM = 't'
MEETING = 'm'
SEMINAR = 's'
TYPE_OF_ACTIVITY = (
    (TRAINING_PROGRAM, _('Training Program')),
    (MEETING, _('Meeting')),
    (SEMINAR, _('Seminar')),
)


class ProjectActivities(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    local = models.ForeignKey(Institution, verbose_name=_('Local'), blank=True, null=True)
    type_of_activity = models.CharField(_('Type of activity'), max_length=1, choices=TYPE_OF_ACTIVITY, blank=True)

    def __unicode__(self):
        return u'%s' % self.title


class News(models.Model):
    """
    An instance of this class is a link to a publication related to a project activity.

    """
    activity = models.ForeignKey(ProjectActivities)
    url = models.URLField(_('URL'))

    def __unicode__(self):
        return u'%s' % self.url

    class Meta:
        verbose_name = _('Link')
        verbose_name_plural = _('Links')
        ordering = ('url', )


class Meeting(ProjectActivities):
    """
    An instance of this class is a meeting.

    """
    # import CEPID name
    cepid_name = settings.CEPID_NAME

    # fields
    broad_audience = models.BooleanField(_('Broad audience?'), default=False)
    cepid_event = models.BooleanField(_('Organized by '+cepid_name+'?'), default=False)
    participant = models.ManyToManyField(Person, verbose_name=_('Participant'), blank=True, null=True)
    description = models.TextField(_('Description'))
    start_date = models.DateField(_('Start date'))
    end_date = models.DateField(_('End date'))

    class Meta:
        verbose_name = _('Meeting')
        verbose_name_plural = _('Meetings')
        ordering = ('-start_date', )

    # Sets the type of activity as Meeting
    def save(self, *args, **kwargs):
        self.type_of_activity = MEETING
        super(Meeting, self).save(*args, **kwargs)


class TrainingProgram(ProjectActivities):
    """
    An instance of this class is a training program.

    """
    speaker = models.ManyToManyField(Person, verbose_name=_('Speaker'))
    meeting = models.ForeignKey(Meeting, verbose_name=_('Meeting'), blank=True, null=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    start_date = models.DateField(_('Start date'))
    end_date = models.DateField(_('End date'), blank=True, null=True)
    duration = models.CharField(_('Duration'), max_length=5, choices=DURATION)
    other_duration = models.CharField(_('Other duration time'), max_length=5, blank=True, null=True,
                                      help_text='E.g.: 11h or 11h30')
    number_of_participants = models.IntegerField(_('Number of participants'), blank=True, null=True)

    class Meta:
        verbose_name = _('Training Program')
        verbose_name_plural = _('Training Programs')
        ordering = ('-start_date', )

    # Sets the type of activity as Training Program
    def save(self, *args, **kwargs):
        self.type_of_activity = TRAINING_PROGRAM
        super(TrainingProgram, self).save(*args, **kwargs)

    def speakers(self):
        return format_html("<br>".join([
            str(speaker) + str(" / " + speaker.institution.__unicode__() if speaker.institution else "")
            for speaker in self.speaker.all()]))

    speakers.allow_tags = True


class SeminarType(models.Model):
    """
    An instance of this class is a type of seminar.

    """
    name = models.CharField(_('Name'), max_length=255)

    # Returns the name
    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('Type of seminar')
        verbose_name_plural = _('Types of seminar')
        ordering = ('name', )


class Seminar(ProjectActivities):
    """
    An instance of this class is a seminar.

    """
    speaker = models.ManyToManyField(Person, verbose_name=_('Speaker'))
    meeting = models.ForeignKey(Meeting, verbose_name=_('Meeting'), blank=True, null=True)
    category = models.ForeignKey(SeminarType, verbose_name=_('Category'))
    international_guest_lecturer = models.BooleanField(_('International guest lecturer?'), default=False)
    abstract = models.TextField(_('Abstract'), blank=True, null=True)
    date = models.DateField(_('Date'))
    time = models.TimeField(_('Time'), blank=True, null=True)
    attachment = models.FileField(_('Attachment'), blank=True, null=True)
    room = models.CharField(_('Room'), max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _('Seminar')
        verbose_name_plural = _('Seminars')
        ordering = ('-date', )

    # Sets the type of activity as Seminar
    def save(self, *args, **kwargs):
        self.type_of_activity = SEMINAR
        super(Seminar, self).save(*args, **kwargs)

    def speakers(self):
        return format_html("<br>".join([
            str(speaker) + str(" / " + speaker.institution.__unicode__() if speaker.institution else "")
            for speaker in self.speaker.all()]))

    speakers.allow_tags = True