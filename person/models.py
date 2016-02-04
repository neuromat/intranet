from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from validation import CPF


def validate_cpf(value):
    """
    Check if the CPF is valid
    """
    validation = CPF(value)
    if not validation.isValid():
        raise ValidationError(_('%s is not a valid CPF') % value)


class Role(models.Model):
    """
    An instance of this class is a role of a person.

    '__unicode__'		Returns the name.
    'class Meta'		Sets the description model (singular and plural) and define ordering of data by name.
    """
    name = models.CharField(_('Name'), max_length=255)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        ordering = ('name', )


class InstitutionType(models.Model):
    """
    An instance of this class is a type of institution.

    '__unicode__'		Returns the name.
    'class Meta'		Sets the description model (singular and plural) and define ordering of data by name.
    """
    name = models.CharField(_('Name'), max_length=255)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('Type of institution')
        verbose_name_plural = _('Types of institution')
        ordering = ('name', )


class Institution(models.Model):
    """
    An instance of this class represents an institution.

    '__unicode__'		        Returns the name. If the institution belongs to another institution, then show the
                                acronym or the name of this institution.
    'get_person_institution'    Used at the reports. The system tries to show only the acronym of the institution.
                                If there isn't an acronym, then it shows the name.
    'class Meta'		        Sets the description model (singular and plural) and and define ordering of data by name.
    """
    name = models.CharField(_('Name'), max_length=255)
    acronym = models.CharField(_('Acronym'), max_length=50, blank=True, null=True)
    type = models.ForeignKey(InstitutionType, verbose_name=_('Type'))
    belongs_to = models.ForeignKey('self', verbose_name=_('Belongs to'), blank=True, null=True)

    def __unicode__(self):
        if self.belongs_to:
            if self.belongs_to.belongs_to:
                if self.belongs_to.acronym and self.belongs_to.belongs_to.acronym:
                    return u'%s - %s/%s' % (self.name, self.belongs_to.acronym, self.belongs_to.belongs_to.acronym)
                elif self.belongs_to.acronym and not self.belongs_to.belongs_to.acronym:
                    return u'%s - %s/%s' % (self.name, self.belongs_to.acronym, self.belongs_to.belongs_to.name)
                elif not self.belongs_to.acronym and self.belongs_to.belongs_to.acronym:
                    return u'%s - %s/%s' % (self.name, self.belongs_to.name, self.belongs_to.belongs_to.acronym)
                elif not self.belongs_to.acronym and not self.belongs_to.belongs_to.acronym:
                    return u'%s - %s/%s' % (self.name, self.belongs_to.name, self.belongs_to.belongs_to.name)
            else:
                if self.belongs_to.acronym:
                    return u'%s / %s' % (self.name, self.belongs_to.acronym)
                else:
                    return u'%s / %s' % (self.name, self.belongs_to.name)
        else:
            return u'%s' % self.name

    def get_person_institution(self):
        if self.belongs_to:
            if self.belongs_to.belongs_to:
                if self.belongs_to.acronym and self.belongs_to.belongs_to.acronym:
                    return u'%s - %s/%s' % (self.name, self.belongs_to.acronym, self.belongs_to.belongs_to.acronym)
                elif self.belongs_to.acronym and not self.belongs_to.belongs_to.acronym:
                    return u'%s - %s/%s' % (self.name, self.belongs_to.acronym, self.belongs_to.belongs_to.name)
                elif not self.belongs_to.acronym and self.belongs_to.belongs_to.acronym:
                    return u'%s - %s/%s' % (self.name, self.belongs_to.name, self.belongs_to.belongs_to.acronym)
                elif not self.belongs_to.acronym and not self.belongs_to.belongs_to.acronym:
                    return u'%s - %s/%s' % (self.name, self.belongs_to.name, self.belongs_to.belongs_to.name)
            else:
                if self.acronym and self.belongs_to.acronym:
                    return u'%s-%s' % (self.acronym, self.belongs_to.acronym)
                elif not self.acronym and self.belongs_to.acronym:
                    return u'%s-%s' % (self.name, self.belongs_to.acronym)
                elif self.acronym and not self.belongs_to.acronym:
                    return u'%s-%s' % (self.acronym, self.belongs_to.name)
                elif not self.acronym and not self.belongs_to.acronym:
                    return u'%s-%s' % (self.name, self.belongs_to.name)
        else:
            if self.acronym:
                return u'%s' % self.acronym
            else:
                return u'%s' % self.name

    class Meta:
        verbose_name = _('Institution')
        verbose_name_plural = _('Institutions')
        ordering = ('name',)


class CitationName(models.Model):
    """
    An instance of this class represents a citation name used by a person
    """
    name = models.CharField(_('Name in bibliographic citation'), max_length=255, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('Citation name')
        verbose_name_plural = _('Citation name')
        ordering = ('name', )


class Person(models.Model):
    """
    An instance of this class represents a person that is a member or a visitor.

    '__unicode__'		Returns the full name.
    'save'              Copy the value of the email and save this value in the email field of the User class (from
                        custom_auth app). This is used because of the function "Forgotten your password or username?"
                        at the login page. This function looks for an email field in the User class.
    'class Meta'		Sets the description (singular and plural) model and the ordering of data by user.
    """
    role = models.ForeignKey(Role, verbose_name=_('Role'), blank=True, null=True)
    institution = models.ForeignKey(Institution, verbose_name=_('Institution'), blank=True, null=True)
    full_name = models.CharField(_('Full name'), unique=True, max_length=255)
    email = models.EmailField(_('Email'), blank=True, null=True)
    citation_name = models.ForeignKey(CitationName, verbose_name=_('Name in bibliographic citation'), blank=True,
                                      null=True, help_text='E.g.: Silva, J.')
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

    def __unicode__(self):
        return u'%s' % self.full_name

    # Get the value of the email and put it in the email field of the User class.
    def save(self, *args, **kw):
        if self.pk is not None:
            orig = Person.objects.get(pk=self.pk)
            if orig.email != self.email:
                from custom_auth.models import User
                user = User.objects.get(user_profile=orig.pk)
                user.email = self.email
                user.save()
        super(Person, self).save(*args, **kw)

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('Person')
        ordering = ('full_name',)