from django.contrib import admin

from profiles.models import *

admin.site.register(GroupMembership)


class GroupMembershipInline(admin.TabularInline):
    model = GroupMembership
    extra = 1


class OrganisationGroupInline(admin.TabularInline):
    model = OrganisationGroup


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    inlines = [
        GroupMembershipInline,
    ]


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    inlines = [
        OrganisationGroupInline,
    ]


@admin.register(BaseGroup, OrganisationGroup)
class BaseGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [
        GroupMembershipInline,
    ]


@admin.register(Shroom)
class ShroomAdmin(admin.ModelAdmin):
    list_display = ('organisation', 'user', 'api_url', 'is_self')
