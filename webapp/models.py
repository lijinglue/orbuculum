# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.db import transaction


class Prediction(models.Model):
    DRAFT = 0
    STAGED = 5
    OPEN = 10
    CLOSED = 15
    SETTLED = 20

    STATUS_CHOICES = (
        (DRAFT, 'DRAFT'),
        (STAGED, 'STAGED'),
        (OPEN, 'OPEN'),
        (CLOSED, 'CLOSED'),
        (SETTLED, 'SETTLED')
    )
    owner = models.ForeignKey('auth.User', related_name='predictions', on_delete=models.PROTECT)
    content = models.CharField(unique=False, max_length=512, blank=False, default='')
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)
    start_at = models.DateTimeField('Open at', blank=True, default=timezone.now, editable=True)
    close_at = models.DateTimeField('Close at', blank=True, default=timezone.now, editable=True)
    created = models.DateTimeField(blank=True, auto_now_add=True)

    def validate_prediction(self, validated_option_ids):
        """
        :param validated_option_ids:
        :return:
        """
        with transaction.atomic():
            self.status = Prediction.SETTLED
            for option in self.options.all():
                if option.id in validated_option_ids:
                    option.resolve()
                else:
                    option.reject()
            self.save()

    def update_open_close_status(self):
        """
        Update the status of current prediction if the start_time/close_time is passed
        :return:
        """
        if self.status == Prediction.STAGED and timezone.now() > self.start_at:
            self.status = Prediction.OPEN
        elif self.status == Prediction.OPEN and timezone.now() > self.close_at:
            self.status = Prediction.CLOSED
        self.save()

    def get_pending_position(self):
        return sum([opt.get_position_bucket()
                    for opt in self.options.filter(status=Position.PENDING_PREDICTION)])

    def get_position(self):
        return sum([opt.get_position_bucket()
                    for opt in self.options.all()])

    def get_options_position(self):
        return [' {0}@{1} '.format(opt.content, opt.get_position_bucket()) for opt in
                self.options.filter(prediction=self)]

    class Meta:
        ordering = ('created',)


class Account(models.Model):
    owner = models.OneToOneField('auth.User', related_name='account', on_delete=models.CASCADE)
    alias = models.CharField(default='Default Account', max_length=32)
    balance = models.FloatField(default=.0)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(blank=True, auto_now_add=True)

    def get_owner_name(self):
        return self.owner.username

    def get_pending_prediction_amount(self):
        return sum([pos.amount for pos in self.positions.filter(status=Position.PENDING_PREDICTION)])

    get_pending_prediction_amount.short_description = 'Amount On Hold'

    def get_pending_clear_amount(self):
        return sum([pos.amount for pos in self.positions.filter(status=Position.PENDING_CLEARING)])

    get_pending_clear_amount.short_description = 'Pending Clearing'

    def __str__(self):
        return "{0} - {1}".format(self.owner.username, self.alias)

    class Meta:
        ordering = ('created',)


class Option(models.Model):
    PENDING = 0
    RESOLVED = 5
    REJECTED = 10
    STATUS_CHOICES = (
        (PENDING, 'PENDING'),
        (RESOLVED, 'RESOLVED'),
        (REJECTED, 'REJECTED'),
    )
    prediction = models.ForeignKey(Prediction, related_name='options', on_delete=models.CASCADE)
    content = models.CharField(unique=False, max_length=128, blank=False, default='')
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)

    def __unicode__(self):
        return self.get_option_full_name()

    def resolve(self):
        """
        Transaction ensured by Prediction
        :return:
        """
        self.status = Option.RESOLVED
        # Pending position for prediction
        total_bucket = self.prediction.get_pending_position()

        # Pending position for this option
        option_bucket = self.get_pending_position()
        for pos in self.positions.filter(status=Position.PENDING_PREDICTION):
            pos.payoff = round(total_bucket * (pos.amount / option_bucket), 2)
            pos.status = Position.PENDING_CLEARING
            pos.save()
            pos.clear_position()

    def reject(self):
        for pos in self.positions.filter(status=Position.PENDING_PREDICTION):
            pos.status = Position.LOSS_CLOSED
            pos.save()

    def get_pending_position(self):
        return sum(
            [position.amount
             for position in self.positions.filter(
                status=Position.PENDING_PREDICTION)])

    def get_position_bucket(self):
        return sum([position.amount for position in self.positions.all()])

    get_position_bucket.short_description = 'position bucket'

    def get_option_full_name(self):
        return "{0}:{1}".format(self.content, self.prediction.content)

    get_option_full_name.short_description = 'option'


class Position(models.Model):
    PENDING_PREDICTION = 0
    LOSS_CLOSED = 3
    PENDING_CLEARING = 5
    CLEARED = 10
    CLEAR_FAILED = 100

    STATUS_CHOICES = (
        (PENDING_PREDICTION, 'PENDING_PREDICTION'),
        (PENDING_CLEARING, 'PENDING_CLEARING'),
        (CLEARED, 'CLEARED'),
        (CLEAR_FAILED, 'CLEAR_FAILED')
    )
    option = models.ForeignKey(Option, related_name='positions', on_delete=models.PROTECT)
    account = models.ForeignKey(Account, related_name='positions', on_delete=models.PROTECT)
    owner = models.ForeignKey('auth.User', related_name='positions', on_delete=models.PROTECT)
    amount = models.FloatField(default=0.0)
    payoff = models.FloatField(default=0.0)
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING_PREDICTION)
    clear_timestamp = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True)

    def clear_position(self):
        """
        Resolve not cleared position when a Prediction can be validated
        :return:
        """
        self.account.balance += self.payoff
        self.status = Position.CLEARED
        self.clear_timestamp = timezone.now()
        self.account.save()
        self.save()

    def get_owner_name(self):
        return self.owner.username

    get_owner_name.short_description = 'Name'

    def get_option_full_name(self):
        return "{0}:{1}".format(self.option.content, self.option.prediction.content)

    get_option_full_name.short_description = 'option'

    def get_profit(self):
        return self.payoff - self.amount

    get_profit.short_description = 'Profit on Maturity'
