# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


@staticmethod
def autocomplete_search_fields():
    return ("id__iexact", "username__icontains",)


User.autocomplete_search_fields = autocomplete_search_fields


class DisplayNameMixin(object):
    def __str__(self):
        if self.name == 'unnamed':
            return "{name} {type} {id}".format(name=self.name, type=self._meta.verbose_name, id=self.id)
        else:
            return self.name

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "name__icontains",)


class Character(DisplayNameMixin, models.Model):
    name = models.CharField(default='unnamed', max_length=64)
    description = models.CharField(default='a character description', max_length=1024)
    avatar = models.ImageField(upload_to='norns.media')


class Dialogue(DisplayNameMixin, models.Model):
    name = models.CharField(default='unnamed', max_length=64, unique=True)
    content = models.CharField(default="dialogue content", max_length=2048)
    character = models.ForeignKey(Character, null=True)


class Option(DisplayNameMixin, models.Model):
    name = models.CharField(default='unnamed', max_length=64)
    dialogue = models.ForeignKey(Dialogue, related_name='options')
    customScripts = models.CharField(max_length=2048)
    nextDialogue = models.ForeignKey(Dialogue, null=True, blank=True)


class Player(DisplayNameMixin, models.Model):
    owner = models.ForeignKey(User, related_name='players', on_delete=models.PROTECT)
    avatar = models.ImageField(upload_to='norns.media')
    name = models.CharField(default='unnamed', max_length=32, unique=True)

    luck = models.IntegerField(default=50)
    intel = models.IntegerField(default=50)
    fortune = models.IntegerField(default=50)
    charisma = models.IntegerField(default=50)
    health = models.IntegerField(default=50)


class CharacterRel(models.Model):
    player = models.ForeignKey(Player, unique=True, related_name='characterRels')
    char = models.ForeignKey(Character)
    friendship = models.IntegerField(default=50)
