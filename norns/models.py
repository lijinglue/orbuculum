# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Character(models.Model):
    name = models.CharField(default='unnamed character', max_length=64)
    avatar = models.CharField(default='', max_length=2048)


class Dialogue(models.Model):
    content = models.CharField(default="dialogue content", max_length=2048)
    character = models.ForeignKey(Character, null=True)


class Option(models.Model):
    dialogue = models.ForeignKey(Dialogue, related_name='options')
    customScripts = models.CharField(max_length=2048)
    nextDialogue = models.ForeignKey(Dialogue, null=True)


class Player(models.Model):
    account = models.OneToOneField('auth.User', related_name='player', on_delete=models.PROTECT)
    avatar = models.CharField(default='', max_length=2048)
    nickname = models.CharField(default='player unknown', max_length=16, unique=True)

    luck = models.IntegerField(default=50)
    intel = models.IntegerField(default=50)
    fortune = models.IntegerField(default=50)
    charisma = models.IntegerField(default=50)
    health = models.IntegerField(default=50)


class CharacterRel(models.Model):
    player = models.ForeignKey(Player, related_name='characterRels')
    char = models.ForeignKey(Character)
    friendship = models.IntegerField(default=50)

