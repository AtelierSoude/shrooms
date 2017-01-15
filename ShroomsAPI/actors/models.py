from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models


# Create your models here.


class ActorGroup(models.Model):
    """
    Group
    """
    owner = models.ForeignKey(
        'Profile',
        related_name='owned_groups',
        on_delete=models.CASCADE)
    members = models.ManyToManyField(
        'Profile',
        verbose_name='group members',
        through='GroupMembership',
        blank=False
    )


class GroupMembership(models.Model):
    """
    Group / Profile many-to-many relationship through model
    """
    member = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE)
    group = models.ForeignKey(
        'ActorGroup',
        on_delete=models.CASCADE)


class Profile(models.Model):
    """
    Profile is an abstract class to contain an
    individual's or organisation's informations
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name='user',
        related_name='profile',
        null=True,
        blank=True
    )
    groups = models.ManyToManyField(
        'ActorGroup',
        verbose_name='groups',
        through='GroupMembership',
        blank=False
    )
    phone_number = models.CharField(
        max_length=10,
        null=False,
        blank=True
    )
    newsletter_subscription = models.BooleanField(default=False)
    email = models.EmailField(
        null=False,
        blank=False
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
    # address = ????


class Individual(Profile):
    """
    Profile subclass that contains a
    person's informations
    """
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
            (0, 'Femme'),
            (1, 'Homme'),
        )
    )


class Adherent(Individual):
    """
    Individual subclass that contains informations
    about registered adherents
    """
    STAFF = 'Staff'
    MEMBER = 'Adhérents'
    STATUS = (
        (
            STAFF, (
                ('Bénévole', 'Bénévole')
            )
        ),
        (
            MEMBER, (
                ('Participant', 'Participant'),
                ('Membre d\'honneur', 'Membre d\'honneur')
            )
        )
    )
    status = models.CharField(
        max_length=20,
        blank=False,
        null=False
    )
    subscription_date = models.DateField(
        auto_now_add=True,
        null=False
    )


class Organisation(Profile):
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

class Shroom(Organisation):
    """
    Organisation subclass that defines a Shroom identity
    """
    pass

class Collaborator(Organisation):
    """
    Organisation subclass that defines a collaborator identity
    """