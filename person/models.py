from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cities_light.models import City

from person.validation import CPF


DEFAULT_CHOICES = ((True, 'Yes'), (False, 'No'))


def validate_cpf(value):
    """
    Check if the CPF is valid
    """
    validation = CPF(value)
    if not validation.isValid():
        raise ValidationError(_('%s is not a valid CPF') % value)
    else:
        pass


class Role(models.Model):
    """
    An instance of this class is a role of a person.

    '__str__'		Returns the name.
    'class Meta'		Sets the description model (singular and plural) and define ordering of data by name.
    """
    name = models.CharField(_('Name'), max_length=255)

    def __str__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        ordering = ('name', )


class InstitutionType(models.Model):
    """
    An instance of this class is a type of institution.

    '__str__'		Returns the name.
    'class Meta'		Sets the description model (singular and plural) and define ordering of data by name.
    """
    name = models.CharField(_('Name'), max_length=255,)

    def __str__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('Type of institution')
        verbose_name_plural = _('Types of institution')
        ordering = ('name', )


class Institution(models.Model):
    """
    An instance of this class represents an institution.

    '__str__'		        Returns the name. If the institution belongs to another institution, then show the
                                acronym or the name of this institution.
    'get_person_institution'    Used at the reports. The system tries to show only the acronym of the institution.
                                If there isn't an acronym, then it shows the name.
    'class Meta'		        Sets the description model (sing. and plural) and and define ordering of data by name.
    """
    name = models.CharField(_('Name'), max_length=255)
    acronym = models.CharField(_('Acronym'), max_length=50, blank=True, null=True)
    type = models.ForeignKey(InstitutionType, verbose_name=_('Type'), on_delete=models.PROTECT)
    belongs_to = models.ForeignKey(
        'self',
        verbose_name=_('Belongs to'),
        blank=True,
        null=True,
        on_delete=models.PROTECT)
    zipcode = models.CharField(_('Zip Code'), max_length=9, blank=True)
    street = models.CharField(_('Address'), max_length=255, blank=True)
    street_complement = models.CharField(_('Complement'), max_length=255, blank=True)
    number = models.CharField(_('Number'), max_length=10, blank=True)
    district = models.CharField(_('District'), max_length=255, blank=True)
    city = models.ForeignKey(City, verbose_name=_('City'), blank=True, null=True, on_delete=models.PROTECT)

    def __str__(self):
        if self.belongs_to:
            if self.belongs_to.belongs_to:
                if self.belongs_to.acronym and self.belongs_to.belongs_to.acronym:
                    return u'%s - %s/%s' % (self.name, self.belongs_to.acronym, self.belongs_to.belongs_to.acronym)
                elif self.belongs_to.acronym and not self.belongs_to.belongs_to.acronym:
                    return u'%s - %s/%s' % (self.name, self.belongs_to.acronym, self.belongs_to.belongs_to.name)
                elif not self.belongs_to.acronym and self.belongs_to.belongs_to.acronym:
                    return u'%s - %s/%s' % (self.name, self.belongs_to.name, self.belongs_to.belongs_to.acronym)
                else:  # elif not self.belongs_to.acronym and not self.belongs_to.belongs_to.acronym:
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
                else:  # elif not self.belongs_to.acronym and not self.belongs_to.belongs_to.acronym:
                    return u'%s - %s/%s' % (self.name, self.belongs_to.name, self.belongs_to.belongs_to.name)
            else:
                if self.acronym and self.belongs_to.acronym:
                    return u'%s-%s' % (self.acronym, self.belongs_to.acronym)
                elif not self.acronym and self.belongs_to.acronym:
                    return u'%s-%s' % (self.name, self.belongs_to.acronym)
                elif self.acronym and not self.belongs_to.acronym:
                    return u'%s-%s' % (self.acronym, self.belongs_to.name)
                else:  # elif not self.acronym and not self.belongs_to.acronym:
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


class Person(models.Model):
    """
    An instance of this class represents a person that is a member or a visitor.

    '__str__'		Returns the full name.
    'save'              Copy the value of the email and save this value in the email field of the User class (from
                        custom_auth app). This is used because of the function "Forgotten your password or username?"
                        at the login page. This function looks for an email field in the User class.
    'class Meta'		Sets the description (singular and plural) model and the ordering of data by user.
    """
    role = models.ForeignKey(Role, verbose_name=_('Role'), blank=True, null=True, on_delete=models.PROTECT)
    institution = models.ForeignKey(
        Institution,
        verbose_name=_('Institution'),
        blank=True,
        null=True,
        on_delete=models.PROTECT)
    full_name = models.CharField(_('Full name'), unique=True, max_length=255)
    email = models.EmailField(_('Email'), blank=True, null=True)
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
    signature = models.ImageField(_('Signature'), upload_to='signatures/', blank=True, null=True)

    def __str__(self):
        return u'%s' % self.full_name

    # Get the value of the email and put it in the email field of the User class.
    def save(self, *args, **kw):
        if self.pk is not None:
            orig = Person.objects.get(pk=self.pk)
            if orig.email != self.email:
                from custom_auth.models import User
                try:
                    user = User.objects.get(user_profile=orig.pk)
                    user.email = self.email
                    user.save()
                except User.DoesNotExist:
                    pass

        super(Person, self).save(*args, **kw)

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('Person')
        ordering = ('full_name',)


class CitationName(models.Model):
    """
    An instance of this class represents a citation name used by a person
    """
    person = models.ForeignKey(Person, verbose_name=_('Name'), on_delete=models.CASCADE)
    name = models.CharField(_('Name in bibliographic citation'), max_length=255)
    default_name = models.BooleanField(_('Default name?'), choices=DEFAULT_CHOICES, max_length=3, default=False)

    def __str__(self):
        return u'%s' % self.name

    def save(self, *args, **kwargs):
        if self.default_name:
            try:
                citations = CitationName.objects.filter(person=self.person)
                citation_default = citations.get(default_name=True)
                citation_default.default_name = False
                citation_default.save()
            except CitationName.DoesNotExist:
                pass
        super(CitationName, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Citation name')
        verbose_name_plural = _('Citation name')
        ordering = ('person', )
