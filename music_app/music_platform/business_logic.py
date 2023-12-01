from .models import *
from .miscellaneous import  get_user_choices, set_user_plays
from django.conf import settings
from .celery_tasks import music_cacher
import json 


def get_music_data(user: object):
    user_liked_songs = get_user_choices(user.id)
    NUMBER_OF_ARTISTS = int(settings.NUMBER_OF_ARTISTS)
    NUMBER_OF_SONGS_PER_ARTIST = int(settings.NUMBER_OF_SONGS_PER_ARTIST) 

    if not settings.REDIS_CONNECTION.exists(f"{settings.CACHE_PREFIX_USER}_{user.id}") and not user_liked_songs:
        random_data = {
            "lower_limit":1,
            "upper_limit":Artists.objects.all().count(),
            "N":NUMBER_OF_ARTISTS
        }
        result = music_cacher.delay(user_id = user.id, NUMBER_OF_SONGS_PER_ARTIST=NUMBER_OF_SONGS_PER_ARTIST, random_request=True, random_data=random_data)
        try:
            result.get(timeout=60)
            inst = set_user_plays(user_liked_songs = [], user_id=user.id)
        except Exception as e:
            print("Timeout exceeded")
            return []
        

    if not settings.REDIS_CONNECTION.exists(f"{settings.CACHE_PREFIX_USER}_{user.id}") and user_liked_songs:
        ml_data = {
            "data":user_liked_songs,
            "N":NUMBER_OF_ARTISTS 
        }

        result = music_cacher.delay(ml_data=ml_data, user_id=user.id, NUMBER_OF_SONGS_PER_ARTIST=NUMBER_OF_SONGS_PER_ARTIST)
        try:
            result.get(timeout=60)
            inst = set_user_plays(user_liked_songs = user_liked_songs, user_id=user.id)
        except Exception as e:
            print(e)
            return []


    tracks_data = json.loads(settings.REDIS_CONNECTION.get(f"{settings.CACHE_PREFIX_USER}_{user.id}"))

    return tracks_data

