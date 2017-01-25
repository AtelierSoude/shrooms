from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.managers import InheritanceManager


class BaseGroup(models.Model):
    """
    Group
    """
    members = models.ManyToManyField(
        'UserProfile',
        verbose_name='members',
        through='GroupMembership',
        blank=False,
    )
    name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name=_('name'),
    )
    # Django Model Utils' Inheritance manager
    objects = InheritanceManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("group")


class OrganisationGroup(BaseGroup):
    """
    Group that represents affiliation to an organisation
    """
    organisation = models.OneToOneField(
        'Organisation',
        blank=False,
        null=False,
        verbose_name=_('organisation'),
    )

    class Meta:
        verbose_name = _('Organisation group')
        verbose_name_plural = _('Organisation groups')


class GroupMembership(models.Model):
    """
    Group / Profile many-to-many relationship through model
    """
    member = models.ForeignKey(
        'UserProfile',
        on_delete=models.CASCADE,
        verbose_name=_('member'),
    )
    group = models.ForeignKey(
        'BaseGroup',
        on_delete=models.CASCADE,
        verbose_name=_('group'),
    )
    is_admin = models.BooleanField(
        default=False,
        verbose_name=_('is admin'),
    )

    def __str__(self):
        return "%s.%s [%s]" % (self.member, self.group, "Admin" if self.is_admin else "Member")

    class Meta:
        verbose_name = _('group membership')
        verbose_name_plural = _('group memberships')


class AbstractProfile(models.Model):
    """
    Profile is an abstract class to contain an
    individual's or organisation's informations
    """

    phone_number = models.CharField(
        max_length=10,
        null=False,
        blank=True,
        verbose_name=_('phone number'),
    )

    date_created = models.DateTimeField(
        null=False,
        blank=True,
        editable=False,
        auto_now_add=True,
        verbose_name=_('date created'),
    )
    about = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('about'),
    )
    website = models.URLField(
        blank=True,
        verbose_name=_('website'),
    )
    # address = ????

    class Meta:
        abstract = True


class UserProfile(AbstractProfile):
    """
    Profile subclass that contains a
    person's informations
    """
    FEMALE = 'Femme'
    MALE = 'Homme'
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        related_name='profile',
        null=False,
        blank=False
    )
    groups = models.ManyToManyField(
        'BaseGroup',
        verbose_name=_('groups'),
        through='GroupMembership',
        blank=False
    )
    first_name = models.CharField(
        max_length=50,
        blank=True,
        null=False,
        verbose_name=_('first name'),
    )
    last_name = models.CharField(
        max_length=50,
        null=False,
        blank=True,
        verbose_name=_('last name'),
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('birth date'),
    )
    gender = models.NullBooleanField(
        choices=(
            (0, FEMALE),
            (1, MALE),
        ),
        verbose_name=_('gender'),
    )
    newsletter_subscription = models.BooleanField(
        default=False,
        verbose_name=_('newsletter'),
    )

    # Django Model Utils' Inheritance manager
    objects = InheritanceManager()

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        verbose_name = _("user profile")
        verbose_name_plural = _("user profiles")


class Organisation(AbstractProfile):
    """
    Profile subclass that contains an
    organisation's informations
    """
    short_name = models.CharField(
        max_length=20,
        blank=True,
        null=False,
        verbose_name=_('short name'),
    )
    full_name = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name=_('full name'),
    )
    type = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name=_('type'),
    )
    email = models.EmailField(blank=True, null=True)
    main_contact = models.ForeignKey(
        'UserProfile',
        blank=True,
        null=True,
        verbose_name=_('main contact'),
    )

    # Django Model Utils' Inheritance manager
    objects = InheritanceManager()

    def __str__(self):
        return "%s" % (self.full_name,)

    class Meta:
        verbose_name = _('Organisation')

