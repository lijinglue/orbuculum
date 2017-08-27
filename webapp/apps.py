# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from django.db.models.signals import post_init


class WebappConfig(AppConfig):
    name = 'webapp'

    def ready(self):
        from .signals import prediction_post_init


class PdConfig(object):
    MINIMUM_POSITION = 10
