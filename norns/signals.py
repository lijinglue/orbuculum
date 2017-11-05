from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Player
from constance import config



@receiver(post_save, sender=User)
def user_post_create(sender, **kwargs):
    user = kwargs['instance']
    # automatically create account for new user
    if kwargs['created'] and config.AUTO_CREATE_ACCOUNT:
        Player.objects.create(owner=user)
