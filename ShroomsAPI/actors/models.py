from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models

from allauth.account.models import EmailAddress
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.managers import InheritanceManager


class BaseGroup(models.Model):
    """
    Group
    """
    members = models.ManyToManyField(
        'UserProfile',
        verbose_name='group members',
        through='GroupMembership',
        blank=False
    )
    name = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )
    # Django Model Utils' Inheritance manager
    objects = InheritanceManager()

    def __str__(self):
        return self.name


class OrganisationGroup(BaseGroup):
    """
    Group that represents affiliation to an organisation
    """
    organisation = models.ForeignKey(
        'Organisation',
        blank=False,
        null=False
    )


class GroupMembership(models.Model):
    """
    Group / Profile many-to-many relationship through model
    """
    member = models.ForeignKey(
        'UserProfile',
        on_delete=models.CASCADE)
    group = models.ForeignKey(
        'BaseGroup',
        on_delete=models.CASCADE)
    is_admin = models.BooleanField(
        default=False
    )

    def __str__(self):
        return "%s.%s [%s]" % (self.member, self.group, "Admin" if self.is_admin else "Member")


class AbstractProfile(models.Model):
    """
    Profile is an abstract class to contain an
    individual's or organisation's informations
    """

    phone_number = models.CharField(
        max_length=10,
        null=False,
        blank=True
    )

    date_created = models.DateTimeField(
        null=False,
        blank=True,
        editable=False,
        auto_now_add=True
    )
    about = models.CharField(
        max_length=255,
        blank=True
    )
    website = models.URLField(
        blank=True
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
        verbose_name='user',
        related_name='profile',
        null=False,
        blank=False
    )
    groups = models.ManyToManyField(
        'BaseGroup',
        verbose_name='groups',
        through='GroupMembership',
        blank=False
    )
    first_name = models.CharField(
        max_length=50,
        blank=True,
        null=False
    )
    last_name = models.CharField(
        max_length=50,
        null=False,
        blank=True
    )
    birth_date = models.DateField(
        null=True,
        blank=True
    )
    gender = models.NullBooleanField(
        choices=(
            (0, FEMALE),
            (1, MALE),
        )
    )
    newsletter_subscription = models.BooleanField(default=False)

    # Django Model Utils' Inheritance manager
    objects = InheritanceManager()

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Organisation(AbstractProfile):
    """
    Profile subclass that contains an
    organisation's informations
    """
    short_name = models.CharField(
        max_length=20,
        blank=True,
        null=False
    )
    full_name = models.CharField(
        max_length=50,
        blank=False,
        null=False
    )
    type = models.CharField(
        max_length=50,
        blank=False,
        null=False
    )
    main_contact = models.ForeignKey(
        'UserProfile',
        blank=True,
        null=True
    )

    # Django Model Utils' Inheritance manager
    objects = InheritanceManager()

    def __str__(self):
        return "%s" % (self.full_name,)


class Shroom(Organisation):
    """
    Organisation subclass that defines a Shroom identity
    """
    api_url = models.URLField(
        verbose_name='API URL'
    )
    # Shared data : use django's content_type fwk ?
