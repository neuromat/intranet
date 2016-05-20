from django.db import models
from django.utils.translation import ugettext_lazy as _
from person.models import Person


# Defining types of media
INTERNAL = 'i'
EXTERNAL = 'e'
TYPE_OF_MEDIA = (
    (INTERNAL, _('Internal')),
    (EXTERNAL, _('External')),
)


class Topic(models.Model):
    """
    An instance of this class is a topic used in a publication.

    'class Meta'		Sets the description model (singular and plural) and define ordering of data by name.
    """
    name = models.CharField(_('Name'), max_length=255)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')
        ordering = ('name', )


class Dissemination(models.Model):
    """
    An instance of this class is a publication in a media outlet.

    '__unicode__'		Returns the title.
    'class Meta'		Defines ordering of data by title.
    """
    title = models.CharField(_('Title'), max_length=255)
    date = models.DateField(_('Date'))
    topic = models.ManyToManyField(Topic, verbose_name=_('Topic'), blank=True)
    link = models.URLField(_('URL'), blank=True, null=True)
    type_of_media = models.CharField(_('Type of media'), max_length=1, choices=TYPE_OF_MEDIA, blank=True)

    def __unicode__(self):
        return u'%s' % self.title

    class Meta:
        ordering = ('title', )

    def topics(self):
        return ', '.join([unicode(topic) for topic in self.topic.all()])


class InternalMediaOutlet(models.Model):
    """
    An instance of this class is an internal media outlet.

    '__unicode__'		Returns the name.
    'class Meta'		Sets the description model (singular and plural) and defines ordering of data by name.
    """
    name = models.CharField(_('Name'), max_length=255)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('Internal media outlet')
        verbose_name_plural = _('Internal media outlets')
        ordering = ('name', )


class Internal(Dissemination):
    """
    An instance of this class is a dissemination using an internal media outlet.

    'class Meta'		Sets the description model (singular and plural).
    'authors'           Get the authors of the publication.
    """
    media_outlet = models.ForeignKey(InternalMediaOutlet, verbose_name=_('Media outlet'))
    author = models.ManyToManyField(Person, verbose_name=_('Author'), blank=True)

    class Meta:
        verbose_name = _('Internal')
        verbose_name_plural = _('Internal')

    # Sets the type of dissemination as Internal
    def save(self, *args, **kwargs):
        self.type_of_media = INTERNAL
        super(Internal, self).save(*args, **kwargs)

    def authors(self):
        return ', '.join([unicode(author) for author in self.author.all()])


class ExternalMediaOutlet(models.Model):
    """
    An instance of this class is an external media outlet.

    '__unicode__'		Returns the name.
    'class Meta'		Sets the description model (singular and plural) and defines ordering of data by name.
    """
    name = models.CharField(_('Name'), max_length=255)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('External media outlet')
        verbose_name_plural = _('External media outlets')
        ordering = ('name', )


class External(Dissemination):
    """
    An instance of this class is a dissemination using an external media outlet.

    'class Meta'		Sets the description model (singular and plural).
    'authors'           Get the authors of the publication.
    """
    media_outlet = models.ForeignKey(ExternalMediaOutlet, verbose_name=_('Media outlet'))
    author = models.ManyToManyField(Person, verbose_name=_('Author'), blank=True)

    class Meta:
        verbose_name = _('External')
        verbose_name_plural = _('External')

    # Sets the type of dissemination as External
    def save(self, *args, **kwargs):
        self.type_of_media = EXTERNAL
        super(External, self).save(*args, **kwargs)

    def authors(self):
        return ', '.join([unicode(author) for author in self.author.all()])
