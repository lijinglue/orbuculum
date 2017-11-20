from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Player, GameState
from constance import config
import random
import string


def create_player(user):
    player = Player.objects.create(
        name=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        , owner=user)
    GameState.objects.create(player=player)


@receiver(post_save, sender=User)
def user_post_create(sender, **kwargs):
    user = kwargs['instance']
    # automatically create account for new user
    if kwargs['created'] and config.AUTO_CREATE_ACCOUNT:
        create_player(user)
