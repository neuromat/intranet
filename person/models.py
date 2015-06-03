from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from validation import CPF


def validate_cpf(value):
    """
    Checks if the CPF is valid

    """
    validation = CPF(value)
    if not validation.isValid():
        raise ValidationError(_('%s is not a valid CPF') % value)


class Role(models.Model):
    """
    An instance of this class is the role of a person.

    '__unicode__'		Returns the name.
    'class Meta'		Sets the description (singular and plural) model and the ordering of data by name.
    """
    name = models.CharField(_('Name'), max_length=255)

    # Returns the name
    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        ordering = ('name', )


class InstitutionType(models.Model):
    """
    An instance of this class is the type of institution.

    '__unicode__'		Returns the name.
    'class Meta'		Sets the description (singular and plural) model and the ordering of data by name.
    """
    name = models.CharField(_('Name'), max_length=255)

    # Returns the name
    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('Type of institution')
        verbose_name_plural = _('Types of institution')
        ordering = ('name', )


class Institution(models.Model):
    """
    An instance of this class represents an institution.

    '__unicode__'		Returns the acronym or the name.
    'class Meta'		Sets the description (singular and plural) model and the ordering of data by acronym.
    """
    name = models.CharField(_('Name'), max_length=255)
    acronym = models.CharField(_('Acronym'), max_length=50, blank=True, null=True)
    type = models.ForeignKey(InstitutionType, verbose_name=_('Type'))
    belongs_to = models.ForeignKey('self', verbose_name=_('Belongs to'), blank=True, null=True)

    # If exists, returns the acronym, if not returns the name
    def __unicode__(self):
        if self.belongs_to:
            if self.acronym:
                return u'%s-%s' % (self.acronym, self.belongs_to)
            else:
                return u'%s-%s' % (self.name, self.belongs_to)
        else:
            if self.acronym:
                return u'%s' % self.acronym
            else:
                return u'%s' % self.name

    class Meta:
        verbose_name = _('Institution')
        verbose_name_plural = _('Institutions')
        ordering = ('-acronym',)


class Person(models.Model):
    """
    An instance of this class represents a person that is a member or a visitor.

    '__unicode__'		Returns the full name.
    'class Meta'		Sets the description (singular and plural) model and the ordering of data by user.
    """
    role = models.ForeignKey(Role, verbose_name=_('Role'), blank=True, null=True)
    institution = models.ForeignKey(Institution, verbose_name=_('Institution'), blank=True, null=True)
    first_name = models.CharField(_('Fisrt name'), max_length=255)
    last_name = models.CharField(_('Last name'), max_length=255)
    email = models.EmailField(_('Email'), blank=True, null=True)
    citation_name = models.CharField(_('Name in bibliographic citation'), max_length=255, blank=True, null=True,
                                     help_text='E.g.: Silva, J.')
    rg = models.CharField(_('RG'), max_length=12, blank=True, null=True)
    cpf = models.CharField(_('CPF'), blank=True, null=True, max_length=15, validators=[validate_cpf])
    passport = models.CharField(_('Passport'), max_length=12, blank=True, null=True)
    phone = models.CharField(_('Phone'), max_length=15, blank=True, null=True)
    cellphone = models.CharField(_('Cell Phone'), max_length=15, blank=True, null=True)
    zipcode = models.CharField(_('Zip Code'), max_length=9, blank=True, null=True)
    street = models.CharField(_('Address'), max_length=255, blank=True, null=True)
    street_complement = models.CharField(_('Complement'), max_length=255, blank=True, null=True)
    number = models.CharField(_('Number'), max_length=10, blank=True, null=True)
    district = models.CharField(_('District'), max_length=255, blank=True, null=True)
    city = models.CharField(_('City'), max_length=255, blank=True, null=True)
    state = models.CharField(_('State'), max_length=255, blank=True, null=True)
    country = models.CharField(_('Country'), max_length=255, blank=True, null=True)

    # Returns the full name
    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    # Description of the model / Sort by user
    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('Person')
        ordering = ('first_name', 'last_name')