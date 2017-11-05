# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from __future__ import unicode_literals
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views.generic import View
from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import NotFound, ValidationError
from oauth2_provider.contrib.rest_framework import IsAuthenticatedOrTokenHasScope
from django.utils.translation import ugettext_lazy as _

from .serializers import *
from constance import config


# Create your views here.

class CharacterView(generics.RetrieveAPIView):
    serializer_class = CharacterSerializer


class PlayerView(generics.RetrieveUpdateAPIView):
    serializer_class = PlayerSerializer


class DialogueView(generics.RetrieveAPIView):
    serializer_class = DialogueSerializer

class CharacterRelView(generics.RetrieveUpdateAPIView):
    serializer_class = CharacterRelSerializer
