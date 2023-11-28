from .models import *
from .miscellaneous import object_filter_orderby,object_filter, get_user_choices, get_image
import requests
from django.conf import settings
from .celery_tasks import music_cacher
import json 
import time
def allowed_music_view(request:any)->list:
    """
    this function returns a list of objects where objects are music objects which the current user has access to  a specific user has access to, this takes the parameter request used in your views,
    this is done to query unique keys such as email,id of a specific user
    """
    allowed_music_objects=[]
    # Querying public music
    allowed_music_objects+=object_filter_orderby({"music_type":"public"},"music_uploads_model",orderby="-date_time")
    # Querying private music
    allowed_music_objects+=object_filter_orderby({"music_type":"private","owner_email_id":request.user.email},"music_uploads_model",orderby="-date_time")
    # Querying protected music where our logged in user is allowed to see
    allowed_music_objects+=object_filter_orderby({"protected_accessors__email":request.user.email},model="music_uploads_model",orderby="-date_time")# Current user permission to music_ids
    # Protected music is still visible to the owner even if he doesn't belong to the allowed email list
    allowed_music_objects+=object_filter_orderby({"owner_email_id":request.user.email,"music_type":"protected"},model="music_uploads_model",orderby="-date_time")
    return allowed_music_objects


def get_music_data(user: object):
    user_liked_songs = get_user_choices(user.id)
    NUMBER_OF_ARTISTS = 1 # Number of Artists you want from ML
    NUMBER_OF_SONGS_PER_ARTIST = 2 # Number of songs per recommended artist you want from spotify

    if not settings.REDIS_CONNECTION.exists(f"{settings.CACHE_PREFIX_USER}_{user.id}") and not user_liked_songs:
        random_data = {
            "lower_limit":1,
            "upper_limit":Artists.objects.all().count(),
            "N":NUMBER_OF_ARTISTS
        }
        result = music_cacher.delay(user_id = user.id, NUMBER_OF_SONGS_PER_ARTIST=NUMBER_OF_SONGS_PER_ARTIST, random_request=True, random_data=random_data)
        try:
            result.get(timeout=30)
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
            result.get(timeout=30)
        except Exception as e:
            print("Timeout exceeded")
            return []


    tracks_data = json.loads(settings.REDIS_CONNECTION.get(f"{settings.CACHE_PREFIX_USER}_{user.id}"))

    return tracks_data

