from django.contrib.auth.models import User
from django.db.models.signals import post_init, post_save
from django.dispatch import receiver
from webapp.models import Prediction, Account
from constance import config


@receiver(post_init, sender=Prediction)
def prediction_post_init(sender, **kwargs):
    prediction = kwargs['instance']
    prediction.update_open_close_status()


@receiver(post_save, sender=User)
def user_post_create(sender, **kwargs):
    user = kwargs['instance']
    # automatically create account for new user
    if kwargs['created'] and config.AUTO_CREATE_ACCOUNT:
        Account.objects.create(owner=user)
