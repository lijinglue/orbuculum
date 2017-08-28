# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views.generic import View
from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import NotFound, ValidationError
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope, IsAuthenticatedOrTokenHasScope
from django.utils.translation import ugettext_lazy as _

from serializers import *
from constance import config


class AccountListView(generics.ListAPIView):
    serializer_class = AccountSerializer
    permission_classes = (IsAuthenticatedOrTokenHasScope,)

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user)


class AccountCreateView(generics.CreateAPIView):
    serializer_class = AccountSerializer
    permission_classes = (IsAuthenticatedOrTokenHasScope,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PredictionRetrieveById(generics.RetrieveAPIView):
    serializer_class = PredictionSerializer

    def get_queryset(self):
        return Prediction.objects.all()


class PredictionRetrieveAll(generics.ListAPIView):
    serializer_class = PredictionSerializer
    paginate_by = 5

    def get_queryset(self):
        return Prediction.objects.all()


class PredictionUpdate(generics.CreateAPIView, generics.UpdateAPIView):
    serializer_class = PredictionSerializer
    permission_classes = (permissions.IsAdminUser,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PositionViews(generics.ListAPIView):
    serializer_class = PositionSerializer
    permission_classes = (IsAuthenticatedOrTokenHasScope,)

    def get_queryset(self):
        user = self.request.user
        return Position.objects.filter(owner=user)


class PredictionPositionViews(generics.CreateAPIView, generics.ListAPIView):
    serializer_class = PositionSerializer
    permission_classes = (IsAuthenticatedOrTokenHasScope,)

    def get_queryset(self):
        user = self.request.user
        oid = self.kwargs['oid']
        try:
            option = Option.objects.get(id=oid)
        except Option.DoesNotExist:
            raise NotFound(_('Option not found'))
        return Position.objects.filter(owner=user,
                                       option=option)

    def perform_create(self, serializer):
        oid = self.kwargs['oid']
        option = Option.objects.get(id=oid)
        account = Account.objects.filter(owner=self.request.user).first()
        amount = self.request.data['amount']

        if option.prediction.status != Prediction.OPEN:
            raise NotFound(
                {'msg': 'Prediction does not exist or is not opened'},
                9000)

        if amount < config.MINIMUM_POSITION or amount > account.balance:
            raise ValidationError(
                {'amount': ['insufficient funds']},
                9000)

        with transaction.atomic():
            account.balance -= amount
            account.save()
            serializer.save(owner=self.request.user,
                            account=account,
                            option=option)


class TopAccountViews(generics.ListAPIView):
    serializer_class = TopAccountSerializer

    def get_queryset(self):
        return Account.objects.filter(is_active=True).annotate(
            profit=(Sum('positions__payoff') - Sum('positions__amount'))
        ).filter(profit__gte=0).order_by('profit')[:10]


class PredictionOptionListViews(generics.ListAPIView):
    serializer_class = OptionRespSerializer

    def get_queryset(self):
        pid = self.kwargs['pid']
        p = Prediction.objects.get(id=pid)
        return Option.objects.filter(prediction=p).annotate(
            option_bucket=Sum('positions__amount'))


class PredictionValidateAdminView(View):
    permission_classes = (permissions.IsAdminUser,)
    def get(self, request, *args, **kwargs):
        template_name = 'admin/validate_prediction.html'
        prediction = Prediction.objects.get(id=int(kwargs['id']))
        return render(request,
                      template_name,
                      {'prediction': prediction, 'next': request.GET['next']})

    def post(self, request, *args, **kwargs):
        next = request.POST['next']
        opt_ids = request.POST['opt[]']
        if isinstance(opt_ids, basestring):
            opt_ids = (int(opt_ids),)
        else:
            opt_ids = (int(opt_id) for opt_id in opt_ids)

        prediction_id = request.POST['prediction']
        prediction = Prediction.objects.get(id=prediction_id)
        prediction.validate_prediction(opt_ids)
        return redirect(next)
