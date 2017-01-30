from django.contrib import admin

from adherents.models import Adherent, Subscription, SubscriptionType, AdherentStatus
from profiles.admin import GroupMembershipInline

# Register your models here.


class SubscriptionInline(admin.TabularInline):
    model = Subscription
    extra=1


@admin.register(AdherentStatus)
class AdherentStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(SubscriptionType)
class SubscriptionTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'status')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'adherent', 'date_begin', 'subscription_type', 'date_end', 'is_active')

@admin.register(Adherent)
class AdherentAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    inlines = [
        GroupMembershipInline,
        SubscriptionInline
    ]
