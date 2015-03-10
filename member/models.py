from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from validation import CPF
from django.db.models import signals
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
    """
    An instance of this class is the role of a user

    '__unicode__'		Returns the name.
    'class Meta'		Sets the description (singular and plural) model and the ordering of data by name.
    """
    name = models.CharField(_('Name'), max_length=50)

    # Returns the name
    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        ordering = ('name', )


class Institution(models.Model):
    """
    An instance of this class represents an University

    '__unicode__'		Returns the name.
    'class Meta'		Sets the description (singular and plural) model and the ordering of data by name.
    """
    name = models.CharField(_('Name'), max_length=100)
    acronym = models.CharField(_('Acronym'), max_length=50, blank=True, null=True)

    # Returns the name
    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('Institution')
        verbose_name_plural = _('Institutions')
        ordering = ('name', )


class Department(models.Model):
    """
    An instance of this class represents a department from an University

    '__unicode__'		Returns the name.
    'class Meta'		Sets the description (singular and plural) model and the ordering of data by name.
    """
    institution = models.ForeignKey(Institution, verbose_name=_('Institution'), blank=True, null=True)
    name = models.CharField(_('Name'), max_length=100)
    acronym = models.CharField(_('Acronym'), max_length=50, blank=True, null=True)

    # Returns the name
    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')
        ordering = ('name', )


class Investigator(models.Model):

    """
    An instance of this class represents an investigator.

    '__unicode__'		Returns the full name from User class.
    'class Meta'		Sets the description (singular and plural) model and the ordering of data by name.
    'create_user_profile_signal' and 'password_change_signal' force password change on first login.
    """
    user = models.OneToOneField(User, verbose_name=_('User'))
    force_password_change = models.BooleanField(_('Force password change'), default=True,
                                                help_text=_('Force the user to change their password at next login.'))
    is_nira_admin = models.BooleanField(_('NIRA admin'), default=False,
                                        help_text=_('Designates whether the user can create content on behalf of '
                                                    'another user.'))
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

    # Post_save signal that will create an Investigator every time a User is created.
    def create_user_profile_signal(sender, instance, created, **kwargs):
        if created:
            Investigator.objects.create(user=instance)

    # If user exists and he is not superuser, checks if the password was changed to modify
    # force_password_change to False.
    def password_change_signal(sender, instance, **kwargs):
        try:
            if User.objects.all().count() == 0:
                return

            user = User.objects.get(username=instance.username)

            if user.is_superuser:
                return

            if not user.password == instance.password:
                profile, created = Investigator.objects.get_or_create(user=user)
                profile.force_password_change = False
                profile.save()
        except User.DoesNotExist:
            pass

    signals.pre_save.connect(password_change_signal, sender=User, dispatch_uid='accounts.models')
    signals.post_save.connect(create_user_profile_signal, sender=User, dispatch_uid='accounts.models')

    # Description of the model / Sort by user
    class Meta:
        verbose_name = _('Personal info')
        verbose_name_plural = _('Personal info')
        ordering = ('user', )


class BibliographicCitation(models.Model):
    """
    An instance of this class represents a name used in a bibliographic citation

    '__unicode__'		Returns the name.
    'class Meta'		Sets the description (singular and plural) model and the ordering of data by name.
    """
    name = models.CharField(_('Name'), max_length=50, help_text='E.g.: Silva, J.')
    investigator = models.ForeignKey(Investigator, verbose_name=_('Investigator'))

    # Returns the name
    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('Bibliographic citation')
        verbose_name_plural = _('Bibliographic citations')
        ordering = ('name', )