# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
from webapp.models import Prediction


class PredictionTestCase(TestCase):
    user = None
    def setUp(self):
        pass

    def test_prediction(self):
        prediction = Prediction.objects.create()
