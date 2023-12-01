from .models import *
from django.core.cache import cache
from django.db.models import Q
from django.conf import settings
from django.contrib.auth import get_user_model
import requests
from api.models import PreviousMLUse

User=get_user_model()


def get_user_choices(user_id: int):
    user_obj = UserClicks.objects.filter(user=user_id).order_by("-weight").values("artist_id","weight")
    
    return list(user_obj)

def set_user_plays(user_id: int, user_liked_songs: list[dict]):
    inst = PreviousMLUse.objects.filter(user_id=user_id).first()
    total_plays=sum(map(lambda x: x["weight"] ,user_liked_songs))
    if not inst: 
        inst = PreviousMLUse.objects.create(total_plays=total_plays, user_id=user_id)
    else:
        inst.total_plays = total_plays
    inst.save()

def get_image(image_url):
    if len(image_url) == 0:
        return None
    
    return image_url[0].get("url")

