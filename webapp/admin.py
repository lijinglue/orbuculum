# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url

from django.contrib import admin

# Register your models here.
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html

from .models import *


class OptionAdmin(admin.ModelAdmin):
    model = Option
    list_display = ('id', 'get_position_bucket', 'get_option_full_name')


class AccountAdmin(admin.ModelAdmin):
    model = Account
    list_display = ('id',
                    'get_owner_name',
                    'alias',
                    'balance',
                    'get_pending_prediction_amount',
                    'get_pending_clear_amount'
                    )


class PositionAdmin(admin.ModelAdmin):
    model = Position
    list_display_links = ('id', 'get_owner_name')
    list_display = ('id', 'get_owner_name', 'get_option_full_name', 'amount', 'payoff', 'status')

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = (
            'option', 'account', 'owner', 'status', 'clear_timestamp'
        )
        if obj:  # editing an existing object
            return readonly_fields
        return ()


class OptionInline(admin.TabularInline):
    model = Option
    can_delete = False
    extra = 0
    fields = ('id', 'content', 'get_position_bucket')
    readonly_fields = ('id', 'get_position_bucket',)


class PredictionAdmin(admin.ModelAdmin):
    model = Prediction
    list_display = ('id', 'content', 'get_options_position', 'status', 'prediction_action')
    inlines = [OptionInline, ]

    def get_admin_url(self, obj):
        """
        the url to the Django admin interface for the model instance
        """
        info = (self.opts.app_label, self.opts.model_name)
        return reverse('admin:%s_%s_changelist' % info)

    def prediction_action(self, obj):
        if obj.status == Prediction.OPEN:
            return format_html(
                '<a class="button" href="{}">Validate</a>',
                reverse('pd:validate_prediction',
                        args=[obj.pk]) + '?next=' + self.get_admin_url(obj)
            )
        else:
            return format_html(
                '<a class="button" style="color:grey;background:#d8d9e0;cursor:not-allowed;">Validate</a>'
            )

    prediction_action.short_description = 'Prediction Actions'
    prediction_action.allow_tags = True


admin.site.register(Option, OptionAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Prediction, PredictionAdmin)
