from django.contrib import admin
from actors.models import *
# Register your models here.
admin.site.register(GroupMembership)


class GroupMembershipInline(admin.TabularInline):
    model = GroupMembership
    extra=1



@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    inlines = [
        GroupMembershipInline,
    ]

@admin.register(Organisation, Shroom)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    

    
@admin.register(OrganisationGroup)
class BaseGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [
        GroupMembershipInline,
    ]
