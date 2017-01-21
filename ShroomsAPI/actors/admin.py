from django.contrib import admin
from actors.models import *
# Register your models here.
admin.site.register(GroupMembership)


class GroupMembershipInline(admin.TabularInline):
    model = GroupMembership
    extra=1

@admin.register(Individual, Adherent)
class IndividualAdmin(admin.ModelAdmin):
    list_display = ('full_name',)
    inlines = [
        GroupMembershipInline,
    ]
    def full_name(self, obj):
        return ("%s %s" % (obj.first_name, obj.last_name))
    full_name.short_description = "Full Name"

@admin.register(Organisation, Shroom)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('full_name',)
    inlines = [
        GroupMembershipInline,
    ]
@admin.register(SubscriptionType)
class SubscriptionTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('adherent', 'date_begin', 'subscription_type')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('email',)
    
@admin.register(ActorGroup)
class ActorGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [
        GroupMembershipInline,
    ]