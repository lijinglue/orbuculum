# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Dialogue(models.Model):
    content = models.CharField(default="dialogue content", max_length=2048)


class Option(models.Model):
    dialogue = models.ForeignKey(Dialogue, related_name='options')
    customScripts = models.CharField(max_length=2048)


class Player(models.Model):
    account = models.OneToOneField('auth.User', related_name='player', on_delete=models.PROTECT)
    nickname = models.CharField(default='player unknown', max_length=16, unique=True)


class Stat(models.Model):
    player = models.ForeignKey(Player, related_name='stats')
    name = models.CharField(default="unnamed stat", max_length=32)
    value = models.IntegerField(default="0")
