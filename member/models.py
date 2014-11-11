from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from validation import CPF
from django.contrib.auth.models import User

# Create your models here.


def validate_cpf(value):
    """
    Checks if the CPF is valid

    """
    validation = CPF(value)
    if not validation.isValid():
        raise ValidationError(_('%s is not a valid CPF') % value)


class Role(models.Model):
    name = models.CharField(_('Name'), max_length=50)

    # Returns the name
    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        ordering = ('name', )


class Institution(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    acronym = models.CharField(_('Acronym'), max_length=50, blank=True, null=True)

    # Returns the name
    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('Institution')
        verbose_name_plural = _('Institutions')
        ordering = ('name', )


class Investigator(models.Model):

    """
    An instance of this class represents an investigator.

    '__unicode__'		Returns the full name from User class.
    'class Meta'		Sets the description (singular and plural) model and the ordering of data by name.
    """
    user = models.OneToOneField(User, verbose_name=_('User'))
    nickname = models.CharField(_('Nickname'), max_length=20, blank=True, null=True)
    role = models.ForeignKey(Role, verbose_name=_('Role'), blank=True, null=True)
    institution = models.ForeignKey(Institution, verbose_name=_('Institution'), blank=True, null=True)
    rg = models.CharField(_('RG'), max_length=12, blank=True, null=True)
    cpf = models.CharField(_('CPF'), blank=True, null=True, max_length=15, validators=[validate_cpf])
    passport = models.CharField(_('Passport'), max_length=12, blank=True, null=True)
    phone = models.CharField(_('Phone'), max_length=15, blank=True, null=True)
    cellphone = models.CharField(_('Cell Phone'), max_length=15, blank=True, null=True)
    zipcode = models.CharField(_('Zip Code'), max_length=9, blank=True, null=True)
    street = models.CharField(_('Address'), max_length=100, blank=True, null=True)
    street_complement = models.CharField(_('Complement'), max_length=100, blank=True, null=True)
    number = models.CharField(_('Number'), max_length=10, blank=True, null=True)
    district = models.CharField(_('District'), max_length=100, blank=True, null=True)
    city = models.CharField(_('City'), max_length=50, blank=True, null=True)
    state = models.CharField(_('State'), max_length=50, blank=True, null=True)
    country = models.CharField(_('Country'), max_length=50, blank=True, null=True)

    # Returns the full name from User class
    def __unicode__(self):
        return u'%s %s' % (self.user.first_name, self.user.last_name)

    # Description of the model / Sort by name
    class Meta:
        verbose_name = _('Investigator')
        verbose_name_plural = _('Investigators')
        ordering = ('user', )


class NameCitation(models.Model):
    name = models.CharField(_('Name'), max_length=50)
    investigator = models.ForeignKey(Investigator, verbose_name=_('Investigator'))

    # Returns the name
    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('Name in citation')
        verbose_name_plural = _('Name in citations')
        ordering = ('name', )