from django.db import models
from music_platform.models import custom_user
# from django.conf import settings
# Create your models here.
class PreviousMLUse(models.Model):
    total_plays = models.IntegerField()
    user = models.OneToOneField(custom_user, to_field="id", on_delete=models.CASCADE)