import requests
from requests.adapters import HTTPAdapter
from .models import Artists
from django.conf import settings
from .miscellaneous import get_image
from celery import shared_task
from celery import current_app
import random
import json

app = current_app

@shared_task
def music_cacher(ml_data: dict = {}, user_id: int = None, NUMBER_OF_SONGS_PER_ARTIST: int = 0, random_request: bool = False, random_data: dict = {}):

    if random_request and not random_data:
        return None

    
    session = requests.Session()

    client_id = settings.SPOTIFY_ID
    client_secret = settings.SPOTIFY_SECRET
    token_url = 'https://accounts.spotify.com/api/token'
    token_params = {
    'grant_type': 'client_credentials',
    "client_id":client_id,
    "client_secret":client_secret,
    }

    token_headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    adapter = HTTPAdapter(max_retries=4)
    session.mount("https://", adapter)

    token_response = session.post(token_url, params=token_params, headers=token_headers)

    if token_response.status_code == 200:
        access_token = token_response.json()['access_token']
    else:
        return None

    
    if not random_request:
        data = session.post(url=f"{settings.ML_SERVICE}/get_recommends/", json=ml_data).json()
    else:

        data = [random.randint(random_data["lower_limit"], random_data["upper_limit"]) for _ in range(random_data["N"])]

    data = Artists.objects.filter(id__in = data).values("name","id")
    tracks_data = []
    for obj in data:
        search_api_url = 'https://api.spotify.com/v1/search'
        search_params = {
            'q': obj['name'].replace(' ','+'),
            'type': 'track',
            'market': 'IN',
            'limit': NUMBER_OF_SONGS_PER_ARTIST,
            "include_external": "audio"
        }
        headers = {
            'Authorization': f'Bearer {access_token}' 
        }

        search_response = session.get(search_api_url, params=search_params, headers=headers)
        if search_response.status_code == 200:
            search_response = search_response.json()
            for track in search_response["tracks"]["items"]:
                tracks_data.append(
                    {
                        "id":track["id"],
                        "music_name":track["name"],
                        "url":track["preview_url"],
                        "artist_name":obj["name"],
                        "artist_id":obj["id"],
                        "image": get_image(track.get("album").get("images"))
                    }
                )
    settings.REDIS_CONNECTION.set(f"{settings.CACHE_PREFIX_USER}_{user_id}", json.dumps(tracks_data))
    return True