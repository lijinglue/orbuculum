from django.db.models.signals import post_init
from django.dispatch import receiver
from webapp.models import Prediction


@receiver(post_init, sender=Prediction)
def prediction_post_init(sender, **kwargs):
    prediction = kwargs['instance']
    prediction.update_open_close_status()
    print prediction
