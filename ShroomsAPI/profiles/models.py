import profiles.validators as validators
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from dry_rest_permissions.generics import (allow_staff_or_superuser,
                                           authenticated_users)
from model_utils.managers import InheritanceManager
from profiles.managers import ShroomManager


class BaseGroup(models.Model):
    """
    Group
    """
    members = models.ManyToManyField(
        'UserProfile',
        verbose_name=_('members'),
        through='GroupMembership',
        blank=False,
    )
    name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name=_('name'),
    )
    description = models.CharField(
        max_length=500,
        null=False,
        blank=True,
        verbose_name=_('description')
    )
    # Django Model Utils' Inheritance manager
    objects = InheritanceManager()

    def has_member(self, profile):
        """
        Check if a profile is a member of group.
        """
        try:
            self.members.get(pk=profile.pk)
            return True
        except UserProfile.DoesNotExist:
            return False

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("group")

    """
    DRY permissions
    """

    @staticmethod
    @authenticated_users
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @authenticated_users
    def has_object_read_permission(self, request):
        return True

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False


class OrganisationGroup(BaseGroup):
    """
    Group that represents affiliation to an organisation
    """
    organisation = models.OneToOneField(
        'Organisation',
        blank=False,
        null=False,
        verbose_name=_('organisation'),
        related_name='organisation_group'
    )

    class Meta:
        verbose_name = _('Organisation group')
        verbose_name_plural = _('Organisation groups')

    """
    DRY permissions
    """

    @staticmethod
    @authenticated_users
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @authenticated_users
    def has_object_read_permission(self, request):
        return True

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False


class GroupRole(models.Model):
    """
    Add role information to group membership
    """
    name = models.CharField(
        max_length=50,
        null=True,
        blank=False,
        verbose_name=_('role')
    )
    group = models.ForeignKey(
        'BaseGroup',
        verbose_name=_('group'),
        related_name=_('roles'),
        null=False,
        blank=False
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('role')
        verbose_name_plural = _('roles')

    """
    DRY permissions
    """

    @staticmethod
    @authenticated_users
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @authenticated_users
    def has_object_read_permission(self, request):
        return True

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False


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
    role = models.ForeignKey(
        'GroupRole',
        null=True,
        blank=True,
        verbose_name=_('role'),
        related_name='group_members'
    )

    def __str__(self):
        return "%s.%s [%s]" % (self.member, self.group, "Admin" if self.is_admin else "Member")

    class Meta:
        verbose_name = _('group membership')
        verbose_name_plural = _('group memberships')

    """
    DRY permissions
    """

    @staticmethod
    @authenticated_users
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @authenticated_users
    def has_object_read_permission(self, request):
        return True

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False


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
        null=True,
        verbose_name=_('first name'),
    )
    last_name = models.CharField(
        max_length=50,
        null=True,
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
        verbose_name=_('subscribed to newsletter'),
    )

    # Django Model Utils' Inheritance manager
    objects = InheritanceManager()

    @property
    def can_subscribe(self):
        """
        Check if profile has first and last name
        """
        return False if (self.first_name and self.last_name) is None else True

    def is_group_member(self, group):
        """
        Check if profile is a member of group
        """
        try:
            self.groups.get(pk=group.pk)
            return True
        except BaseGroup.DoesNotExist:
            return False

    def __str__(self):
        if (self.first_name or self.last_name) is not None:
            return "%s %s" % (self.first_name or "", self.last_name or "")
        else:
            return "@%s" % self.user.username

    """
    DRY Permissions
    """

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        "Disable write access except for admins"
        return False

    @staticmethod
    @authenticated_users
    def has_read_permission(request):
        "Allow read access to auth users"
        return True

    @authenticated_users
    def has_object_read_permission(self, request):
        "Allow object read access to auth users"
        return True

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        "Disable object write access except for admins"
        return False

    @allow_staff_or_superuser
    def has_object_update_permission(self, request):
        "Auth user may update their own profile"
        return self.user == request.user

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
    type = models.ForeignKey(
        'OrganisationType',
        blank=False,
        null=False,
        verbose_name=_('organisation type'),
    )
    email = models.EmailField(blank=True, null=True)
    main_contact = models.ForeignKey(
        'UserProfile',
        blank=True,
        null=True,
        verbose_name=_('main contact'),
    )

    def __str__(self):
        return "%s" % (self.full_name,)

    class Meta:
        verbose_name = _('Organisation')

    """
    DRY permissions
    """

    @staticmethod
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    def has_object_read_permission(self, request):
        return True

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False


class OrganisationType(models.Model):
    """
    Available organisation types
    """
    type = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name=_('type'),
    )

    def __str__(self):
        return self.type

    """
    DRY permissions
    """

    @staticmethod
    @authenticated_users
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @authenticated_users
    def has_object_read_permission(self, request):
        return True

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False


class Shroom(models.Model):
    """
    A Shroom identity
    """
    api_url = models.URLField(
        verbose_name=_('API URL')
    )
    organisation = models.OneToOneField(
        Organisation,
        blank=False,
        null=False,
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        related_name='shroom',
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )
    is_self = models.BooleanField(
        _('Set this shroom and organisation as self'),
        default=False,
        validators=[validators.validate_is_self],
    )

    objects = ShroomManager
    # Shared data : use django's content_type fwk ?

    """
    DRY permissions
    """

    @staticmethod
    @authenticated_users
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @authenticated_users
    def has_object_read_permission(self, request):
        return True

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False
